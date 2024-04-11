import json

def getModuleState(path, moduleName: str):
    print(f"Getting {moduleName} resources from components.tfstate")
    with open(path) as f:
        coreState = json.load(f)

        core_resources = []

        for resource in coreState["resources"]:
            if "module" in resource:
                if moduleName in resource['module']:
                    core_resources.append(resource)

        return core_resources

def mergeModuleState(destinationState, addState: list, module: str):
    print(f"Merging {module} resources into core.tfstate")
    with open(destinationState) as f:
        coreState = json.load(f)
        coreResources = coreState["resources"] + addState

        coreState.pop("resources")

        coreState["resources"] = coreResources

        return(json.dumps(coreState, indent=2))