import os
import time

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
                  "statefulset.kubernetes.io/pod-name=%s-0 "
                  %(context,ns, resource_name))

    @staticmethod
    def waitForLBServiceCondition(context, ns, resource_name, timeout):
        print("Waiting (for %is)for LoadBalancer Service %s"%(timeout, resource_name), sep=' ', end='', flush=True)
        ip = KubectlHelper.getLoadBalancerIP(context,ns,resource_name)
        for i in range(timeout):
            print(".", sep=' ', end='', flush=True)
            time.sleep(1)
        print (ip)

    @staticmethod
    def applyYaml(context, ns, file_name):
        os.system("kubectl --context %s -n %s apply -f %s"
                  % (context, ns, file_name))
