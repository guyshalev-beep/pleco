import grpc

from pleco_target_pb2 import K8sGWRequest
from pleco_target_pb2_grpc import K8sGWStub


if __name__ == '__main__':
    print('start')
    channel = grpc.insecure_channel("192.168.50.184:50051")
    #channel = grpc.insecure_channel("localhost:50051")

    client = K8sGWStub(channel)
    request = K8sGWRequest(
        fileName="yaml/sample.yaml1"
    )
    # Get Namespaces - TODO
    ret = client.GetNSs(request)
    print (ret)

    print ("create deployment")
    deploymentRes = client.ApplyDeployment(K8sGWRequest(fileName="yaml/hello-world-deployment.yaml", namespace="test"))
    print (deploymentRes)

    print ("create service ")
    serviceRes = client.ApplyService(K8sGWRequest(fileName="yaml/hello-world-service.yaml", namespace="default"))
    print (serviceRes)
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
