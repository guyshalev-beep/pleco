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
    def config_client(self, config_file):
       config.load_kube_config(config_file)

    def config_client_token(self):
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # Define the bearer token we are going to use to authenticate.
        # See here to create the token:
        # https://kubernetes.io/docs/tasks/access-application-cluster/access-cluster/
        aToken = "eyJhbGciOiJSUzI1NiIsImtpZCI6IlFBR1p2NS1LTzVkb05xQ3VES25fcTJtZmtVZG5LNXRXektXQ05ZUjI0c0kifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4taHc0aGYiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjZlMTYyZDk4LWRjOGEtNDQ1Ni05MGUwLTllZGFmYjRjMDQ4NSIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.4YBJ5UBECgLyB-Ex1Uj_u23EdQnR11u4JPMFpTQCqe8Rql7AKhbn4PLxnWOsgIYuENVpYqLXKpnbrzZ7kJeFnb00vnZvoIr4KyVATVlyU0OU3mxYXSTKIupCjhqebb4IudAdFHC1Pe52rA6sDAWjrtx8auHTRC0R0P1jV8p7zUJQB5zhrZYY8mJMqBF8Iqd8XMh-Jwx2cyCwfTwH3rDkXDnAJyvUowhC_1zPQWluBr3Yl-BIgWEYY6nq9q6knJfe7Fy1WfkCLlS1b_Dlvnt7tyjiyF16mp2JVWdvFpFwC9HKoxOCxi4LzmqVstVueHliZv2owiHmEVmuF_jendx-Jw"

        # Create a configuration object
        aConfiguration = client.Configuration()

        # Specify the endpoint of your Kube cluster
        aConfiguration.host = "https://34.68.232.48:443"

        # Security part.
        # In this simple example we are not going to verify the SSL certificate of
        # the remote cluster (for simplicity reason)
        aConfiguration.verify_ssl = False
        # Nevertheless if you want to do it you can with these 2 parameters
        # configuration.verify_ssl=True
        # ssl_ca_cert is the filepath to the file that contains the certificate.
        # configuration.ssl_ca_cert="certificate"

        aConfiguration.api_key = {"authorization": "Bearer " + aToken}
        return aConfiguration



    def TestConnection(self, request, context):
        aConfiguration = self.config_client_token()
        # Create a ApiClient with our config
        #v1 = client.ApiClient(aConfiguration, header_name="Accept", header_value=["application/xml", "application/json"])
        #aApiClient.select_header_accept(["application/xml", "application/json"])
        my_api_client = client.ApiClient(aConfiguration)
        my_api_client.select_header_accept(["","application/json", "application/yaml", "application/vnd.kubernetes.protobuf"])
        v1 = client.CoreV1Api(aConfiguration)
        v1.__init__(api_client=my_api_client)


        # Do calls
        try:

            print("Listing pods with their IPs:")
            ret = v1.list_pod_for_all_namespaces(watch=False)
 #           dicto = {}
 #           for i in ret.items:
 #               dicto[i.metadata.name] = i.metadata.uid
        except:
            e = sys.exc_info()
            print (e)
            return K8sGWResponse(status=False, msg=str(e))
        return K8sGWResponse(status=True, msg="connection succeed. cwd:'%s'" % os.getcwd())

    def GetNSs(self, request, context):
        print("start ns config")
        try:
           # self.config_client(request.config_file)
            aConfiguration = self.config_client_token()

        except:
            e = sys.exc_info()
            print (e)
            return K8sGWResponse(status=False, msg=str(e))
        print ("after config")
        v1 = client.CoreV1Api(aConfiguration)
        v1.select_header_accept(["application/xml", "application/json"])
        #v1 = client.CoreV1Api()
        dicto = {}
        try:
            ret = v1.list_namespace(watch=False)
            for i in ret.items:
                print("%s\t" % (i.metadata.name))
                dicto[i.metadata.name] = i.metadata.uid
        except:
            e = sys.exc_info()
            print (e)
            return K8sGWResponse(status=False, msg=str(e))

        print ("after")

        return K8sGWResponse(resources=dicto)

    def ApplyDeployment(self, request, context):
        print ("start apply deployment")
        #self.config_client()
        aConfiguration = self.config_client_token()

        print ("after config")
        print (request.fileName)
        try:
            with open(path.join(path.dirname(__file__), request.fileName)) as f:
                dep = yaml.safe_load(f)
                # Create a ApiClient with our config
                my_api_client = client.ApiClient(aConfiguration)
                my_api_client.select_header_accept(
                    ["", "application/json", "application/yaml", "application/vnd.kubernetes.protobuf"])

                k8s_apps_v1 = client.AppsV1Api(aConfiguration)
                k8s_apps_v1.__init__(api_client=my_api_client)
                resp = k8s_apps_v1.create_namespaced_deployment(
                    body=dep,namespace=request.namespace)
                print("Deployment created. status='%s'" % resp.metadata.name)
                return K8sGWResponse(status=True, msg="Deployment created. status='%s'" % resp.metadata.name)
        except:
            e = sys.exc_info()
            return K8sGWResponse(status=False, msg=str(e))
        #return K8sGWResponse(status=False, msg="failed to create deployment '%s'" % request.fileName)

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

        #return K8sGWResponse(status=False, msg="failed to create service")
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
