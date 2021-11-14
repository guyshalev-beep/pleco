import os
import grpc
import sys
import yaml

from kubectl_helper import KubectlHelper

sys.path.append("./pleco_target")
from pleco_target_pb2 import K8sGWRequest
from pleco_target_pb2_grpc import K8sGWStub


def handle_leap_to_new_cluster(sources_doc, step_doc):
    leader_source = [s for s in sources_doc if s['name'] == "leader_source"][0]
    follower_source = [s for s in sources_doc if s['name'] == "follower_source"][0]
    yaml_ = step_doc['resource']['body']
    leader_client = K8sGWStub(grpc.insecure_channel("%s:50051" % leader_source['externalIP']))
    follower_client = K8sGWStub(grpc.insecure_channel("%s:50051" % follower_source['externalIP']))
    ns = step_doc['resource']['namespace']
    resource_name = step_doc['resource']['name']
    resource_np_name = step_doc['resource']['np_name']
    print("start MONGODB handle_leap_to_new_cluster for:%s from leader:%s to follower:%s" % (resource_name,leader_source['externalIP'], follower_source['externalIP']))
    # Create on follower
    # at the moment, my client cant handle statefulset. create with kubectl
    #deployment_res = follower_client.ApplyDeployment(
    #    K8sGWRequest(body=str(yaml), namespace=ns, client_host=follower_source['api_server'], client_port=str(follower_source['port']),
    #                 client_token=follower_source['token']))
    #print(deployment_res)
    KubectlHelper.applyYaml(follower_source['context'], ns, step_doc['resource']['path'])

    KubectlHelper.waitForStatefulsetCondition(follower_source['context'],ns, resource_name)
    p = os.popen("kubectl --context %s -n %s get pods -o custom-columns=PodName:.metadata.name | grep %s" % (follower_source['context'],ns, resource_name))
    mongo_pod = p.read()[:-1]

    print("MONGODB ready with POD = %s" % mongo_pod)
    mongo_follower_host = KubectlHelper.getNodePortIP(follower_source['context'],ns, resource_np_name)
    mongo_leader_host = KubectlHelper.getNodePortIP(leader_source['context'], ns, resource_np_name)
    # LEADER:
    # add follower as secondary
    with open(r"script1_leader.js", 'w') as file:
        documents = yaml.dump("rs.add(\"%s:27017\")"%mongo_follower_host, file)
    os.system("kubectl --context %s cp -n %s script1_leader.js /%s:." % (leader_source['context'], ns, mongo_pod))
    os.system("kubectl --context %s exec -it %s -n %s -- mongo script1_leader.js" % (leader_source['context'],mongo_pod,ns))

    # make follower the primary
    with open(r"script2_leader.js", 'w') as file:
        documents = yaml.dump("cfg = rs.conf(); cfg.members[0].priority = 0.5; cfg.members[1].priority = 1; rs.reconfig(cfg)", file)
    os.system("sleep 10s")
    os.system("kubectl --context %s cp -n %s script2_leader.js /%s:." % (leader_source['context'], ns, mongo_pod))
    os.system("kubectl --context %s exec -it %s -n %s -- mongo script2_leader.js" % (leader_source['context'],mongo_pod,ns))

    # FOLLOWER:
    # remove leader from replicaset
    with open(r"script1_follower.js", 'w') as file:
        documents = yaml.dump("rs.remove(\"%s:27017\")"%mongo_leader_host, file)
    os.system("sleep 10s")
    os.system("kubectl --context %s cp -n %s script1_follower.js /%s:." % (follower_source['context'], ns, mongo_pod))
    os.system("kubectl --context %s exec -it %s -n %s -- mongo script1_follower.js" % (follower_source['context'],mongo_pod,ns))

    print ("Synced Mongo. delete leader")
    # Delete from Leader
    deploymentRes = leader_client.DeleteDeployment(
        K8sGWRequest(resourceName=resource_name, namespace=ns, client_host=leader_source['api_server'],
                     client_port=str(leader_source['port']),
                     client_token=leader_source['token']))
    print(deploymentRes)
# Standalone for redis does not involve any sync. It looks like Standalone Deployment.
def handle_standalone(sources_doc, step_doc):
    # deploy to follower source
    source = [s for s in sources_doc if s['name'] == "follower_source"][0]
    yaml_ = step_doc['resource']['body']
    follower_client = K8sGWStub(grpc.insecure_channel("%s:50051" % source['externalIP']))
    ns = step_doc['resource']['namespace']
    resource_name = step_doc['resource']['name']
    print("start MONGODB handle_standalone for:%s to follower:%s" % (resource_name,source['externalIP']))
    # Create on follower
    deployment_res = follower_client.ApplyDeployment(
        K8sGWRequest(body=str(yaml_), namespace=ns,
                     client_host=source['api_server'], client_port=str(source['port']),
                     client_token=source['token']))
    print(deployment_res)
    os.system("kubectl --context %s -n %s wait --for=condition=ready pod --timeout=60s -l "
              "statefulset.kubernetes.io/pod-name=%ds-0 "
              % (source['context'], ns, resource_name))
class MongoDBHandler(object):
    def __init__(self):
        print("start MongoDBHandler")
        pass

    def handle(self, sources_doc, step_doc):
        method = step_doc['method']
        print("start MONGODB handling with method=%s" % method)
        if method == 'leap_to_new_cluster':
            return handle_leap_to_new_cluster(sources_doc, step_doc)
        if method == 'standalone':
            return handle_standalone(sources_doc, step_doc)
        return None