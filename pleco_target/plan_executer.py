import yaml
import os
from deploment_handler import DeploymentHandler
from service_handler import ServiceHandler
from filesystem_repository_handler import FilesystemRepositoryHandler


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def get_repository_handler(plan_step_doc):
    repository_handler_name = plan_step_doc['resource']['handler']
    print("repository_handler_name=%s" % repository_handler_name)
    if repository_handler_name == 'FilesystemRepositoryHandler':
        return FilesystemRepositoryHandler(method)
    elif repository_handler_name == 'VaultRepositoryHandler':
        pass
    pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("guy")
    print(os.system("pwd"))
with open(r'./pleco_target/plans/plan_a.yaml') as file:
    documents = yaml.full_load(file)
    print(documents)
    handlers_doc = documents.get('handlers')
    sources_doc = documents.get('sources')
    plan = documents.get('plan')
    print(handlers_doc)
    print(sources_doc)

    for plan_step_doc in plan:
        handler = plan_step_doc['handler']
        method = plan_step_doc['method']

        # Repository Handler
        repository_handler = get_repository_handler(plan_step_doc)
        # select the specific resource handler doc which its TYPE equals the plan step's RESOURCE.HANDLER
        #repository_handler_doc = handlers_doc['type' == plan_step_doc['resource']['handler']]
        repository_handler_doc = [s for s in handlers_doc if s['type'] == plan_step_doc['resource']['handler']][0]

        body = repository_handler.handle(repository_handler_doc, plan_step_doc);
   #     print(body)
        plan_step_doc['resource']['body'] = body

        # Handler
        handler_object = DeploymentHandler()  # default
        if handler == "DeploymentHandler":
            handler_object = DeploymentHandler()
        if handler == "ServiceHandler":
            handler_object = ServiceHandler()
        handler_object.handle(sources_doc, plan_step_doc)
