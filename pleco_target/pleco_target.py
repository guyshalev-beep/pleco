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

        print ("before 2")
        print ("working dir: {0}".format(os.getcwd()))

        try:
            config.load_kube_config('config')
        except:
            e = sys.exc_info()
            print (e)

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
