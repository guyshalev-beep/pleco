import grpc

from pleco_target_pb2 import K8sGWRequest
from pleco_target_pb2_grpc import K8sGWStub


def print_hi(name):
    from kubernetes import client, config

    # Configs can be set in Configuration class directly or using helper utility
    config.load_kube_config()

    v1 = client.CoreV1Api()
    print("Listing pods with their IPs:")
    ret = v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('start')
    #print_hi("")
    channel = grpc.insecure_channel("192.168.50.184:50051")
    #channel = grpc.insecure_channel("localhost:50051")

    client = K8sGWStub(channel)
    request = K8sGWRequest(
        user_id=1,  max_results=3
    )
    print ("just a sec")
    ret = client.GetNSs(request)
    print (ret)
    """
    channel = grpc.insecure_channel("192.168.50.13:50051")
    client = K8sGWStub(channel)

    request = K8sGWRequest(
        user_id=1,  max_results=3
    )
    print (client.GetNSs(request))
    """
    #print (client.GetNSs(request))


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
