from kubernetes import client, config
from concurrent import futures
import random
import logging
import os
import sys
from os import path

import yaml
import grpc
from kubernetes.client import ApiException

from pleco_target_pb2 import (
    K8sGWResponse,
    K8sResources,

)
import pleco_target_pb2_grpc

class K8sGWService(
    pleco_target_pb2_grpc.K8sGWServicer
):
    def config_client(self):
        try:
            #config.load_kube_config('config')
            config.load_kube_config('$HOME/.kube/config')
        except:
            e = sys.exc_info()
            print (e)

    def GetNSs(self, request, context):
        try:
            self.config_client()
        except:
            e = sys.exc_info()
            print (e)
            return K8sGWResponse(status=False, msg=str(e))
        print ("after config")
        v1 = client.CoreV1Api()
        dicto ={}
        try:
            ret = v1.list_namespace(watch=False)
            for i in ret.items:
                print("%s\t" % (i.metadata.name))
                dicto[i.metadata.name] = i.metadata.uid
        except:
            e = sys.exc_info()
            print (e)

        print ("after")

        return K8sGWResponse(resources=dicto)

    def ApplyDeployment(self, request, context):
        print ("start apply deployment")
        self.config_client()
        print ("after config")
        print (request.fileName)
        try:
            with open(path.join(path.dirname(__file__), request.fileName)) as f:
                dep = yaml.safe_load(f)
                k8s_apps_v1 = client.AppsV1Api()
                resp = k8s_apps_v1.create_namespaced_deployment(
                    body=dep,namespace=request.namespace)
                print("Deployment created. status='%s'" % resp.metadata.name)
                return K8sGWResponse(status=True, msg="Deployment created. status='%s'" % resp.metadata.name)
        except:
            e = sys.exc_info()
            return K8sGWResponse(status=False, msg=str(e))
        return K8sGWResponse(status=False, msg="failed to create deployment '%s'" % request.fileName)

    def ApplyService(self, request, context):
        print ("start apply service")
        self.config_client()
        print ("after config")
        v1 = client.CoreV1Api()
        try:
            with open(path.join(path.dirname(__file__), request.fileName)) as f:
                dep = yaml.safe_load(f)
                k8s_apps_v1 = client.CoreV1Api()
                resp = k8s_apps_v1.create_namespaced_service(
                    body=dep,namespace=request.namespace)
                print("Service created. status='%s'" % resp.metadata.name)
                return K8sGWResponse(status=True, msg="Service created. status='%s'" % resp.metadata.name)
        except:
            e = sys.exc_info()
            return K8sGWResponse(status=False, msg=str(e))
        print ("after")

        return K8sGWResponse(status=False, msg="failed to create service")
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pleco_target_pb2_grpc.add_K8sGWServicer_to_server(
        K8sGWService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
