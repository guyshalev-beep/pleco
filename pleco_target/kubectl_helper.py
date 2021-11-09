import os
class KubectlHelper(object):
    @staticmethod
    def getLoadBalancerIP(context, ns, resource_lb_name):
        p = os.popen("kubectl --context %s -n %s get service %s -o jsonpath='{.status.loadBalancer.ingress[0].ip}'"
                     % (context, ns, resource_lb_name))
        return p.read()[:-1]

    @staticmethod
    def getNodePortIP(context, ns, resource_np_name):
        p = os.popen("kubectl --context %s -n %s get service %s -o jsonpath='{.spec.clusterIP}'"
                     % (context, ns, resource_np_name))
        mongo_follower_host = p.read()[:-1]

    @staticmethod
    def waitForStatefulsetCondition(context, ns, resource_name):
        os.system("kubectl --context %s -n %s wait --for=condition=ready pod --timeout=60s -l "
                  "statefulset.kubernetes.io/pod-name=%ds-0 "
                  %(context,ns, resource_name))