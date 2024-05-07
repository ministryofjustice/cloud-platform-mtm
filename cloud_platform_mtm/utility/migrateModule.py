from cloud_platform_mtm.utility import utility

import json

def migrate_module_resources(module: str, destination_path, source_path):
    module_name = "module." + module
    module_state = get_module_state(source_path, module_name)

    destination_new_state = merge_module_state(destination_path, module_state, module)
    utility.save_state("core", destination_new_state)

    source_new_state = delete_module_state(source_path, module_name)
    utility.save_state("components", source_new_state)

def get_module_state(path, module_name: str):
    print(f"Getting {module_name} resources from components.tfstate")
    with open(path) as f:
        destination_new_state = json.load(f)

        destination_new_resources = []

        for resource in destination_new_state["resources"]:
            if "module" in resource:
                if module_name in resource['module']:
                    destination_new_resources.append(resource)

        return destination_new_resources

def merge_module_state(destination_state, add_state: list, module: str):
    print(f"Merging {module} resources into core.tfstate")
    with open(destination_state) as f:
        destination_new_state = json.load(f)
        core_resources = destination_new_state["resources"] + add_state

        destination_new_state.pop("resources")

        destination_new_state["resources"] = core_resources

        return(json.dumps(destination_new_state, indent=2))

def delete_module_state(source_path, module_name: str):
    print(f"Removing {module_name} resource from components.tfstate")
    with open(source_path) as f:
        source_new_state = json.load(f)

        source_new_resources = []

        for resource in source_new_state['resources']:
            if "module" in resource:
                if module_name not in resource['module']:
                    dependency_removed_resource = utility.remove_dependencies(resource, module_name)
                    source_new_resources.append(dependency_removed_resource)
            else:
                # Ensure we capture all resources that aren't modules
                source_new_resources.append(resource)

        source_new_state.pop("resources")

        source_new_state["resources"] = source_new_resources

        return(json.dumps(source_new_state, indent=2))
