import json

from cloud_platform_mtm.utility import utility

def deleteModuleState(source_path, module_name: str):
    print(f"Removing {module_name} resource from components.tfstate")
    with open(source_path) as f:
        source_new_state = json.load(f)

        source_new_resources = []

        for resource in source_new_state['resources']:
            if "module" in resource:
                if module_name not in resource['module']:
                    dependencyRemovedResource = utility.remove_dependencies(resource, module_name)
                    source_new_resources.append(dependencyRemovedResource)
            else:
                # Ensure we capture all resources that aren't modules
                source_new_resources.append(resource)

        source_new_state.pop("resources")

        source_new_state["resources"] = source_new_resources

        return(json.dumps(source_new_state, indent=2))
