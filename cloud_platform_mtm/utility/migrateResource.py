import re
import typer
import json

from cloud_platform_mtm.utility import utility

def validate_resource_name(resource_name: str):
    match = re.search(r'\w*\.\S\w*', resource_name)

    if match:
        return True
    else:
        print("Resource does not match expected pattern - resource_type.resource_name")
        raise typer.Exit(code=1)

def migrate_resource(resource_name: str, destination_path, source_path):
    resource_state = get_resource_state(source_path, resource_name)

    destination_new_state = merge_resource_state(destination_path, resource_state, resource_name)
    utility.save_state("core", destination_new_state)

    source_new_state = delete_resource_state(source_path, resource_name)
    utility.save_state("components", source_new_state)


def get_resource_state(path, resource_name: str):
    print(f"Getting {resource_name}")

    split = str.split(resource_name, ".")

    type = split[0]
    name = split[1]

    destination_new_resource = []

    with open(path) as f:
        state = json.load(f)
        for resource in state["resources"]:
            if resource["type"] == type and resource["name"] == name:
                destination_new_resource.append(resource)

    return destination_new_resource

def merge_resource_state(destination_path, resource_state, resource_name):
    print(f"Merging {resource_name}")

    with open(destination_path) as f:
        destination_new_state = json.load(f)
        core_resources = destination_new_state["resources"] + resource_state

        destination_new_state.pop("resources")

        destination_new_state["resources"] = core_resources

        return(json.dumps(destination_new_state, indent=2))

def delete_resource_state(source_path, resource_name):
    split = str.split(resource_name, ".")

    type = split[0]
    name = split[1]

    with open(source_path) as f:
        source_new_state = json.load(f)

        source_new_resources = []

        for resource in source_new_state["resources"]:
            if resource["type"] == type and resource["name"] == name:
                print(f"Removing {resource["type"]}.{resource["name"]}")
            else:
                dependency_removed_resource = utility.remove_dependencies(resource, resource_name)
                source_new_resources.append(dependency_removed_resource)

        source_new_state.pop("resources")

        source_new_state["resources"] = source_new_resources

        return(json.dumps(source_new_state, indent=2))