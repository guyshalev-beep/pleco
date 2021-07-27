from kubernetes import client, config
from concurrent import futures
import random
import logging
import os
import sys

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
            config.load_kube_config('config')
        except:
            e = sys.exc_info()
            print (e)

    def GetNSs(self, request, context):
        self.config_client()
        print ("after config")
        v1 = client.CoreV1Api()
        print("Listing pods with their IPs:")
        dicto ={}
        print (dicto)

        try:
            ret = v1.list_pod_for_all_namespaces(watch=False)
            for i in ret.items:
                print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
                dicto[i.metadata.name] = i.status.pod_ip
        except:
            e = sys.exc_info()
            print (e)

        print ("after")

        return K8sGWResponse(resources=dicto)

    def ApplyDeployment(self, request, context):
        self.config_client()
        print ("after config")
        v1 = client.CoreV1Api()

        try:
            ret = v1.list_pod_for_all_namespaces(watch=False)
            for i in ret.items:
                print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
                dicto[i.metadata.name] = i.status.pod_ip
        except:
            e = sys.exc_info()
            print (e)

        print ("after")

        return K8sGWResponse(resources=dicto)
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
