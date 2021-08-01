import grpc

from pleco_target_pb2 import K8sGWRequest
from pleco_target_pb2_grpc import K8sGWStub


if __name__ == '__main__':
    print('start')

    channel = grpc.insecure_channel("192.168.50.184:50051") #TAL
    channel = grpc.insecure_channel("192.168.50.13:50051") #MAIN
    channel = grpc.insecure_channel("104.197.16.122:50051") #GCP
#TAL
    to = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjNpUVRWdE40TnBFLTlBSlRfNktMbmdQc2NYazFtM3ktLUNIUkR4dWdoM0kifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tOXJuNXAiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjFiNTVkNzM4LWU2MjQtNDc5Zi1hNTVlLThiZTM2MWI4YzQzMiIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.nyc7Kr-jMdXQXR27Mbf44bOoYi5zVKJ0QqYO06jPj--_OUTEs388B3ylr3tXT79Mxc2P0uFR-_JoJ6fo6XMFKvSHbEkTtFpTfxUTfHSX5_GSGitp2u3SYpfEZ3Hva8Bk_VyD-Zg-c2-0381HbIHloPxh9J0nkjBIgG0rhgijOadDl2E9wWXqWn9ew4-SYaogmqyenweQesSf3iheyGtauP9lhxuJ_GR71IPZ96n27Jq1aiG0Ae-C9xp1Do9abNcNjGCZ2mduVqkSnKNBFRAKAJ-hHzyadqpz1tUoE-0NwwtqnxWF7DrQbFDpYIehY_ccHksqY3FwP1AnhiSGOLPaZQ"
#GCP
    to = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjY2MmtSRElYaVFfcUZiT2VwS3VGbEpjQ1VlaWctb3h0ZHVuOGdDMGMwb1EifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4teHJkZ2ciLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6IjYwYjhmMDUxLTc2MTMtNDE1ZC05NzgwLWY1MTBjMDEzNGQyYyIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.O8frRG_Mhhb5vTOaDKvbL9v93K2KoCQdBJiS1lLbD0z9sXJowMcc6wSXP4Vky2gE_gn43Ua9AVbyZ-BAKxO91yIDdLaZlan6optoJczFXJgZxuGHNqrP1arjjiss5lTHgQjEiYTaU9bHNvNDSuZmuim34pBZqZNkVLwnTd0ypsU0eqOM-BsvpmS9DrU4ZKgrVRcm2x96e9_poHhq91wK03GuINjAcjIq97ccIjLjm3jZGSn6l-v0Fl0qH3KyvljE3Q_9kmMevkvAm6rAsXxlcdt8Z98WRvg_rHyA0rRQNiA3LVjYY5HqeVSKIuQR02NBp8-3Zqd3HZFhVtJxYv9kcQ"
#TAL
    ho = "127.0.0.1"
#GCP
    ho = "107.178.210.34"
    #ho = "34.135.3.153"

    po = "443"
    client = K8sGWStub(channel)

    print("Test")
    ret = client.TestConnection(K8sGWRequest())
    print (ret)

    print("Get NS")
    ret = client.GetNSs(K8sGWRequest(config_file="config_dir/config-gcp2", client_host=ho, client_port=po, client_token=to))
    print (ret)

    print ("create deployment")
    deploymentRes = client.ApplyDeployment(K8sGWRequest(fileName="yaml/hw.yaml", namespace="default", client_host=ho, client_port=po, client_token=to))
    print (deploymentRes)
    """
    print ("create service ")
    serviceRes = client.ApplyService(K8sGWRequest(fileName="yaml/hello-world-service.yaml", namespace="default"))
    print (serviceRes)
    
    channel = grpc.insecure_channel("192.168.50.13:50051")
    client = K8sGWStub(channel)

    request = K8sGWRequest(
        user_id=1,  max_results=3
    )
    print (client.GetNSs(request))
    """
    #print (client.GetNSs(request))



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
