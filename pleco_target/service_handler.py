import os
import grpc
import sys
from kubectl_helper import KubectlHelper

sys.path.append("./pleco_target")
from pleco_target_pb2 import K8sGWRequest
from pleco_target_pb2_grpc import K8sGWStub


def handle_leap_to_new_cluster(sources_doc, step_doc):
    leader_source = [s for s in sources_doc if s['name'] == "leader_source"][0]
    follower_source = [s for s in sources_doc if s['name'] == "follower_source"][0]
    yaml = step_doc['resource']['body']
    leader_client = K8sGWStub(grpc.insecure_channel("%s:50051" % leader_source['externalIP']))
    follower_client = K8sGWStub(grpc.insecure_channel("%s:50051" % follower_source['externalIP']))
    ns = step_doc['resource']['namespace']
    resource_name = step_doc['resource']['name']
    # Create on follower
    print("start handle_leap_to_new_cluster for:%s from leader:%s to follower:%s" % (resource_name,leader_source['externalIP'], follower_source['externalIP']))

    service_res = follower_client.ApplyService(
        K8sGWRequest(body=str(yaml) , namespace=ns,
                     client_host=follower_source['api_server'],
                     client_port=str(follower_source['port']),
                     client_token=follower_source['token']))
    print(service_res)

    #os.system("kubectl -n %s wait --for=condition=available service %s --timeout=5m" % (ns, resource_name))

    # Delete from Leader
    serviceRes = leader_client.DeleteService(
        K8sGWRequest(resourceName=resource_name, namespace=ns, client_host=leader_source['api_server'],
                    client_port=str(leader_source['port']), client_token=leader_source['token']))
    print(serviceRes)



def handle_standalone(sources_doc, step_doc):
    # deploy to follower source
    follower_source = [s for s in sources_doc if s['name'] == "follower_source"][0]
    follower_client = K8sGWStub(grpc.insecure_channel("%s:50051" % follower_source['externalIP']))
    leader_source = [s for s in sources_doc if s['name'] == "leader_source"][0]
    leader_client = K8sGWStub(grpc.insecure_channel("%s:50051" % leader_source['externalIP']))
    yaml = step_doc['resource']['body']
    ns = step_doc['resource']['namespace']
    resource_name = step_doc['resource']['name']
    if ("target_cluster" in step_doc['resource']):
        target_cluster_name = step_doc['resource']['target_cluster']
    else:
        target_cluster_name = "follower"
    # Create on follower
    if(target_cluster_name == "leader"):
        client = leader_client
        source = leader_source
    else:
        client = follower_client
        source = follower_source
    print("start handle_standalone for:%s to %s:%s" % (resource_name,target_cluster_name,source['externalIP']))
    service_res = client.ApplyService(
        K8sGWRequest(body=str(yaml), namespace=ns,
                     client_host=source['api_server'],
                     client_port=str(source['port']),
                     client_token=source['token']))
    print(service_res)
  #  os.system("kubectl -n %s wait --for=condition=available deployment %s --timeout=5m" % (ns, resource_name))

def handle_standalone_delete(sources_doc, step_doc):
    follower_source = [s for s in sources_doc if s['name'] == "follower_source"][0]
    follower_client = K8sGWStub(grpc.insecure_channel("%s:50051" % follower_source['externalIP']))
    leader_source = [s for s in sources_doc if s['name'] == "leader_source"][0]
    leader_client = K8sGWStub(grpc.insecure_channel("%s:50051" % leader_source['externalIP']))
    ns = step_doc['resource']['namespace']
    resource_name = step_doc['resource']['name']
    if ("target_cluster" in step_doc['resource']):
        target_cluster_name = step_doc['resource']['target_cluster']
    else:
        target_cluster_name = "follower"
    # Create on follower
    if(target_cluster_name == "leader"):
        client = leader_client
        source = leader_source
    else:
        client = follower_client
        source = follower_source
    print("start handle_standalone_delete for:%s to %s:%s" % (resource_name,target_cluster_name,source['externalIP']))
    serviceRes = leader_client.DeleteService(
        K8sGWRequest(resourceName=resource_name, namespace=ns, client_host=source['api_server'],
                    client_port=str(source['port']), client_token=source['token']))
    print(serviceRes)


class ServiceHandler(object):
    def __init__(self):
        # print("start ServiceHandler")
        pass

    def handle(self, sources_doc, step_doc):
        method = step_doc['method']
        print("ServiceHandler start handling with method=%s" % method)
        if method == 'leap_to_new_cluster':
            return handle_leap_to_new_cluster(sources_doc, step_doc)
        if method == 'standalone':
            return handle_standalone(sources_doc, step_doc)
        if method == 'standalone_delete':
            return handle_standalone_delete(sources_doc, step_doc)
        return None