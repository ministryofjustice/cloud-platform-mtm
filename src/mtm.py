#!/usr/bin/env python3

from pathlib import Path
from typing import Optional

import typer
import json

from typing_extensions import Annotated

def main(
    module: Annotated[str, typer.Option(help="Name of the module to migrate")] = None,
    destinationState: Annotated[Optional[Path], typer.Option(help="Path to the destination tfstate file")] = None,
    sourceState: Annotated[Optional[Path], typer.Option(help="Path to the source tfstate file")] = None,
    #dryrun: Annotated[bool, typer.Option(help="dry run.")] = False,
):
    coreCheck = checkFile(destinationState, "tfstate")
    componentsCheck = checkFile(sourceState, "tfstate")

    if coreCheck == componentsCheck == True:
        migrateResources(module, destinationState, sourceState)

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
        print("The file doesn't exist")

def migrateResources(module: str, destinationState, sourceState):
    moduleState = getModuleState(module, sourceState)

    coreState = mergeModuleState(destinationState, moduleState, module)
    saveState("core", coreState)

    componentsState = deleteModuleState(sourceState, module)
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

        moduleName = "module." + module
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

def deleteModuleState(sourceState, module: str):
    print(f"Removing {module} resource from components.tfstate")
    with open(sourceState) as f:
        componentsState = json.load(f)
        moduleName = "module." + module

        newResource = []

        for resource in componentsState['resources']:
            if "module" in resource:
                if moduleName not in resource['module']:
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
