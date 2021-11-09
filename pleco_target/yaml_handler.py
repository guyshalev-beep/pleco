import os
import grpc
import sys

sys.path.append("./pleco_target")
from pleco_target_pb2 import K8sGWRequest
from pleco_target_pb2_grpc import K8sGWStub
from kubectl_helper import KubectlHelper

def handle_standalone(sources_doc, step_doc):
    # deploy to follower source
    source = [s for s in sources_doc if s['name'] == "follower_source"][0]
    follower_source = [s for s in sources_doc if s['name'] == "follower_source"][0]
    ns = step_doc['resource']['namespace']
    resource_name = step_doc['resource']['name']
    fileName = step_doc['resource']['path']
    print("start handle_standalone for:%s to follower:%s" % (fileName,source['externalIP']))
    KubectlHelper.applyYaml(follower_source['context'],ns,fileName)

class YamlHandler(object):
    def __init__(self):
        # print("start YamlHandler")
        pass

    def handle(self, sources_doc, step_doc):
        method = step_doc['method']
        print("YamlHandler start handling with method=%s" % method)
 #       if method == 'leap_to_new_cluster':
 #           return handle_leap_to_new_cluster(sources_doc, step_doc)
        if method == 'standalone':
            return handle_standalone(sources_doc, step_doc)
        return None