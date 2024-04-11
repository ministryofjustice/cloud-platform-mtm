import json

def deleteModuleState(sourceState, moduleName: str):
    print(f"Removing {moduleName} resource from components.tfstate")
    with open(sourceState) as f:
        componentsState = json.load(f)

        newResource = []

        for resource in componentsState['resources']:
            if "module" in resource:
                if moduleName not in resource['module']:
                    dependencyRemovedResource = removeDependencies(resource, moduleName)
                    newResource.append(dependencyRemovedResource)
            else:
                # Ensure we capture all resources that aren't modules
                newResource.append(resource)

        componentsState.pop("resources")

        componentsState["resources"] = newResource

        return(json.dumps(componentsState, indent=2))

def removeDependencies(resource, moduleName: str):
    for instances in resource:
        if "instances" in instances:
            for instance in resource['instances']:
                if "dependencies" in instance:
                    if any(moduleName in s for s in instance['dependencies']):
                        newDep = [x for x in instance['dependencies'] if moduleName not in x]
                        instance.pop("dependencies")
                        instance["dependencies"] = newDep

    return(resource)