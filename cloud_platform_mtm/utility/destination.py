import json

def getModuleState(path, module_name: str):
    print(f"Getting {module_name} resources from components.tfstate")
    with open(path) as f:
        destination_new_state = json.load(f)

        destination_new_resources = []

        for resource in destination_new_state["resources"]:
            if "module" in resource:
                if module_name in resource['module']:
                    destination_new_resources.append(resource)

        return destination_new_resources

def mergeModuleState(destination_state, add_state: list, module: str):
    print(f"Merging {module} resources into core.tfstate")
    with open(destination_state) as f:
        destination_new_state = json.load(f)
        core_resources = destination_new_state["resources"] + add_state

        destination_new_state.pop("resources")

        destination_new_state["resources"] = core_resources

        return(json.dumps(destination_new_state, indent=2))