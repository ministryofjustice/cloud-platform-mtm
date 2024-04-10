#!/usr/bin/env python3

from pathlib import Path
from typing import Optional

import typer
import json
import re

from typing_extensions import Annotated

def main(
    migrate: Annotated[str, typer.Option] = None,
    core_tfstate: Annotated[Optional[Path], typer.Option()] = None,
    components_tfstate: Annotated[Optional[Path], typer.Option()] = None,
    dryrun: Annotated[bool, typer.Option(help="dry run.")] = False,
):
    coreCheck = checkFile(core_tfstate, "tfstate")
    componentsCheck = checkFile(components_tfstate, "tfstate")

    if coreCheck == componentsCheck == True:
        migrateResources(migrate, core_tfstate, components_tfstate)

def checkFile(file, type: str):
    if file is None:
        print(f"No {type} file")
        raise typer.Abort()
    if file.is_file():
        return True
    elif file.is_dir():
        print("Path is a directory")
        raise typer.Abort()
    elif not file.exists():
        print("The migrate file doesn't exist")

def migrateResources(module: str, core_tfstate, components_tfstate):
    moduleState = getModuleState(module, components_tfstate)

    coreState = mergeModuleState(core_tfstate, moduleState, module)
    saveState("core", coreState)

    componentsState = deleteModuleState(components_tfstate, module)
    saveState("components", componentsState)

def saveState(module: str, state):
    print(f"Saving new state file - {module}New.tfstate")

    fileName = module + "New.tfstate"

    with open(fileName, "w") as text_file:
        text_file.write(state)

def getModuleState(module: str, path):
    print(f"Getting {module} resources from components.tfstate")
    with open(path) as f:
        coreState = json.load(f)

        i = 0

        core_resources = []

        # @TODO refactor, we don't need regex here
        regex = r"module." + module + r".*"
        for resource in coreState["resources"]:
            if "module" in resource:
                if re.match(regex, resource['module']):
                    core_resources.append(resource)
                    i += 1

        return core_resources

def mergeModuleState(core_tfstate, addState: list, module: str):
    print(f"Merging {module} resources into core.tfstate")
    with open(core_tfstate) as f:
        coreState = json.load(f)
        coreResources = coreState["resources"] + addState

        coreState.pop("resources")

        coreState["resources"] = coreResources

        return(json.dumps(coreState, indent=2))

def deleteModuleState(components_tfstate, module: str):
    print(f"Removing {module} resource from components.tfstate")
    with open(components_tfstate) as f:
        componentsState = json.load(f)

        newResource = []

        for resource in componentsState['resources']:
            if "module" in resource:
                if "module.gatekeeper" not in resource['module']:
                    dededResource = removeDependencies(resource, module)
                    newResource.append(dededResource)
            else:
                # Ensure we capture all resources that aren't modules
                newResource.append(resource)

        componentsState.pop("resources")

        componentsState["resources"] = newResource

        return(json.dumps(componentsState, indent=2))

def removeDependencies(resource, module: str):
    moduleName = "module." + module

    for instances in resource:
        if "instances" in instances:
            for instance in resource['instances']:
                if "dependencies" in instance:
                    if any(moduleName in s for s in instance['dependencies']):
                        newDep = [x for x in instance['dependencies'] if moduleName not in x]
                        instance.pop("dependencies")
                        instance["dependencies"] = newDep

    return(resource)

if __name__ == "__main__":
    typer.run(main)
