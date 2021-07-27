from kubernetes import client, config
from concurrent import futures
import random
import logging
import os
import sys

import grpc
from kubernetes.client import ApiException

from pleco_target_pb2 import (
    BookCategory,
    BookRecommendation,
    RecommendationResponse,
    K8sGWResponse,
    K8sResources,

)
import pleco_target_pb2_grpc

books_by_category = {
    BookCategory.MYSTERY: [
        BookRecommendation(id=1, title="The Maltese Falcon"),
        BookRecommendation(id=2, title="Murder on the Orient Express"),
        BookRecommendation(id=3, title="The Hound of the Baskervilles"),
    ],
    BookCategory.SCIENCE_FICTION: [
        BookRecommendation(
            id=4, title="The Hitchhiker's Guide to the Galaxy"
        ),
        BookRecommendation(id=5, title="Ender's Game"),
        BookRecommendation(id=6, title="The Dune Chronicles"),
    ],
    BookCategory.SELF_HELP: [
        BookRecommendation(
            id=7, title="The 7 Habits of Highly Effective People"
        ),
        BookRecommendation(
            id=8, title="How to Win Friends and Influence People"
        ),
        BookRecommendation(id=9, title="Man's Search for Meaning"),
    ],
}


class RecommendationService(
    pleco_target_pb2_grpc.RecommendationsServicer
):
    def Recommend(self, request, context):
        if request.category not in books_by_category:
            context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")

        books_for_category = books_by_category[request.category]
        num_results = min(request.max_results, len(books_for_category))
        books_to_recommend = random.sample(
            books_for_category, num_results
        )

        return RecommendationResponse(recommendations=books_to_recommend)


class K8sGWService(
    pleco_target_pb2_grpc.K8sGWServicer
):
    def GetNSs(self, request, context):

        # Configs can be set in Configuration class directly or using helper utility
        print ("before 2")
        print ("working dir: {0}".format(os.getcwd()))
        try:
            config.load_incluster_config()
        except:
            e = sys.exc_info()
            print (e)
        print ("try again")
        try:
            config.load_kube_config('config')
        except:
            e = sys.exc_info()
            print (e)
        """
        print ("try again2")
        try:
            #ApiToken = 'ZXlKaGJHY2lPaUpTVXpJMU5pSXNJbXRwWkNJNklqTnBVVlJXZEU0MFRuQkZMVGxCU2xSZk5rdE1ibWRRYzJOWWF6RnRNM2t0TFVOSVVrUjRkV2RvTTBraWZRLmV5SnBjM01pT2lKcmRXSmxjbTVsZEdWekwzTmxjblpwWTJWaFkyTnZkVzUwSWl3aWEzVmlaWEp1WlhSbGN5NXBieTl6WlhKMmFXTmxZV05qYjNWdWRDOXVZVzFsYzNCaFkyVWlPaUprWldaaGRXeDBJaXdpYTNWaVpYSnVaWFJsY3k1cGJ5OXpaWEoyYVdObFlXTmpiM1Z1ZEM5elpXTnlaWFF1Ym1GdFpTSTZJbVJsWm1GMWJIUXRkRzlyWlc0dE9YSnVOWEFpTENKcmRXSmxjbTVsZEdWekxtbHZMM05sY25acFkyVmhZMk52ZFc1MEwzTmxjblpwWTJVdFlXTmpiM1Z1ZEM1dVlXMWxJam9pWkdWbVlYVnNkQ0lzSW10MVltVnlibVYwWlhNdWFXOHZjMlZ5ZG1salpXRmpZMjkxYm5RdmMyVnlkbWxqWlMxaFkyTnZkVzUwTG5WcFpDSTZJakZpTlRWa056TTRMV1UyTWpRdE5EYzVaaTFoTlRWbExUaGlaVE0yTVdJNFl6UXpNaUlzSW5OMVlpSTZJbk41YzNSbGJUcHpaWEoyYVdObFlXTmpiM1Z1ZERwa1pXWmhkV3gwT21SbFptRjFiSFFpZlEubnljN0tyLWpNZFhRWFIyN01iZjQ0Yk9vWWk1elZLSjBRcVlPMDZqUGotLV9PVVRFczM4OEIzeWxyM3RYVDc5TXhjMlAwdUZSLV9Kb0o2Zm82WE1GS3ZTSGJFa1R0RnBUZnhVVGZIU1g1X0dTR2l0cDJ1M1NZcGZFWjNIdmE4QmtfVnlELVpnLWMyLTAzODFIYklIbG9QeGg5SjBua2pCSWdHMHJoZ2lqT2FkRGwyRTl3V1hxV245ZXc0LVNZYW9nbXF5ZW53ZVFlc1NmM2loZXlHdGF1UDlsaHh1Sl9HUjcxSVBaOTZuMjdKcTFhaUcwQWUtQzl4cDFEbzlhYk5jTmpHQ1oybWR1VnFrU25LTkJGUkFLQUotaEh6eWFkcXB6MXRVb0UtME53d3RxbnhXRjdEclFiRkRwWUllaFlfY2NIa3NxWTNGd1AxQW5oaVNHT0xQYVpR'
            ApiToken = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjNpUVRWdE40TnBFLTlBSlRfNktMbmdQc2NYazFtM3ktLUNIUkR4dWdoM0kifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tOXJuNXAiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjFiNTVkNzM4LWU2MjQtNDc5Zi1hNTVlLThiZTM2MWI4YzQzMiIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.nyc7Kr-jMdXQXR27Mbf44bOoYi5zVKJ0QqYO06jPj--_OUTEs388B3ylr3tXT79Mxc2P0uFR-_JoJ6fo6XMFKvSHbEkTtFpTfxUTfHSX5_GSGitp2u3SYpfEZ3Hva8Bk_VyD-Zg-c2-0381HbIHloPxh9J0nkjBIgG0rhgijOadDl2E9wWXqWn9ew4-SYaogmqyenweQesSf3iheyGtauP9lhxuJ_GR71IPZ96n27Jq1aiG0Ae-C9xp1Do9abNcNjGCZ2mduVqkSnKNBFRAKAJ-hHzyadqpz1tUoE-0NwwtqnxWF7DrQbFDpYIehY_ccHksqY3FwP1AnhiSGOLPaZQ'
            configuration = client.Configuration()
            configuration.host = 'https://kubernetes.docker.internal:6443'
            configuration.verify_ssl = False
            configuration.debug = True
            # configuration.username = 'guy'
            # configuration.password = 'Canon6dd'
            configuration.api_key_prefix['authorization'] = 'Bearer'
            configuration.api_key = {ApiToken}

            client.Configuration.set_default(configuration)
        except:
            e = sys.exc_info()
            print (e)
        """
        print ("after config")
        v1 = client.CoreV1Api()
        print("Listing pods with their IPs:")
        dicto ={'1111':'a', '2':'b'}
        print (dicto)

        try:
            #ret = v1.list_pod_for_all_namespaces(watch=False)
            ret = v1.list_pod_for_all_namespaces(watch=False)
            for i in ret.items:
                print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
                dicto[i.metadata.name] = i.status.pod_ip
        except:
            e = sys.exc_info()
            print (e)
        """
        ApiToken = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjNpUVRWdE40TnBFLTlBSlRfNktMbmdQc2NYazFtM3ktLUNIUkR4dWdoM0kifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tOXJuNXAiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjFiNTVkNzM4LWU2MjQtNDc5Zi1hNTVlLThiZTM2MWI4YzQzMiIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.nyc7Kr-jMdXQXR27Mbf44bOoYi5zVKJ0QqYO06jPj--_OUTEs388B3ylr3tXT79Mxc2P0uFR-_JoJ6fo6XMFKvSHbEkTtFpTfxUTfHSX5_GSGitp2u3SYpfEZ3Hva8Bk_VyD-Zg-c2-0381HbIHloPxh9J0nkjBIgG0rhgijOadDl2E9wWXqWn9ew4-SYaogmqyenweQesSf3iheyGtauP9lhxuJ_GR71IPZ96n27Jq1aiG0Ae-C9xp1Do9abNcNjGCZ2mduVqkSnKNBFRAKAJ-hHzyadqpz1tUoE-0NwwtqnxWF7DrQbFDpYIehY_ccHksqY3FwP1AnhiSGOLPaZQ'
        configuration = client.Configuration()
        configuration.host = 'https://192.168.50.184:6443'
        configuration.verify_ssl = False
        configuration.debug = True
        # configuration.username = 'guy'
        # configuration.password = 'Canon6dd'
        configuration.api_key_prefix['authorization'] = 'Bearer'
        configuration.api_key = {ApiToken}

        client.Configuration.set_default(configuration)
        kubeApi = client.CoreV1Api()
        try:
            allPods = kubeApi.list_pod_for_all_namespaces(watch=False)
        except ApiException as e:
            print("Exception when calling CoreV1Api->list_pod_for_all_namespaces: %s\n" % e)

        """
      #  config.load_kube_config("~/.kube/config")
        print ("after")
        """
        v1 = client.CoreV1Api()
        print("Listing pods with their IPs:")
        ret = v1.list_pod_for_all_namespaces(watch=False)
        lst1 = ['kkkkk', 'kkkkkkkkk']
        dicto ={'1111':'a', '2':'b'}
        print (dicto)
        lst1[1] = 'i.metadata.namespace'
        print(lst1)
        for i in ret.items:
            print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
            dicto[i.metadata.name] = i.status.pod_ip
          #  lst1[3] = 'i.metadata.namespace'
        return K8sGWResponse(resources=dicto)
"""
        return K8sGWResponse(resources=dicto)
        #return K8sGWResponse(resources={'1111':'a', '777dddd2':'b'})

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pleco_target_pb2_grpc.add_RecommendationsServicer_to_server(
        RecommendationService(), server
    )
    pleco_target_pb2_grpc.add_K8sGWServicer_to_server(
        K8sGWService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
