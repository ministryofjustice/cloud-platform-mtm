import json

def deleteModuleState(sourceState, moduleName: str):
    print(f"Removing {moduleName} resource from components.tfstate")
    with open(sourceState) as f:
        sourceNewState = json.load(f)

        sourceNewResources = []

        for resource in sourceNewState['resources']:
            if "module" in resource:
                if moduleName not in resource['module']:
                    dependencyRemovedResource = removeDependencies(resource, moduleName)
                    sourceNewResources.append(dependencyRemovedResource)
            else:
                # Ensure we capture all resources that aren't modules
                sourceNewResources.append(resource)

        sourceNewState.pop("resources")

        sourceNewState["resources"] = sourceNewResources

        return(json.dumps(sourceNewState, indent=2))

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