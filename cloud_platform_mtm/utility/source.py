import json

from cloud_platform_mtm.utility import utility

def deleteModuleState(sourceState, moduleName: str):
    print(f"Removing {moduleName} resource from components.tfstate")
    with open(sourceState) as f:
        sourceNewState = json.load(f)

        sourceNewResources = []

        for resource in sourceNewState['resources']:
            if "module" in resource:
                if moduleName not in resource['module']:
                    dependencyRemovedResource = utility.remove_dependencies(resource, moduleName)
                    sourceNewResources.append(dependencyRemovedResource)
            else:
                # Ensure we capture all resources that aren't modules
                sourceNewResources.append(resource)

        sourceNewState.pop("resources")

        sourceNewState["resources"] = sourceNewResources

        return(json.dumps(sourceNewState, indent=2))
