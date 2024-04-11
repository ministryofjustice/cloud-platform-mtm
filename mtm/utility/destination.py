import json

def getModuleState(path, moduleName: str):
    print(f"Getting {moduleName} resources from components.tfstate")
    with open(path) as f:
        destinationNewState = json.load(f)

        destinationNewResources = []

        for resource in destinationNewState["resources"]:
            if "module" in resource:
                if moduleName in resource['module']:
                    destinationNewResources.append(resource)

        return destinationNewResources

def mergeModuleState(destinationState, addState: list, module: str):
    print(f"Merging {module} resources into core.tfstate")
    with open(destinationState) as f:
        destinationNewState = json.load(f)
        coreResources = destinationNewState["resources"] + addState

        destinationNewState.pop("resources")

        destinationNewState["resources"] = coreResources

        return(json.dumps(destinationNewState, indent=2))