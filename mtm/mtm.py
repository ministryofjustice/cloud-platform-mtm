#!/usr/bin/env python3

from pathlib import Path
from typing import Optional

import typer
import json

from typing_extensions import Annotated
from utility import utility

def main(
    module: Annotated[str, typer.Option(help="Name of the module to migrate")] = None,
    destinationState: Annotated[Optional[Path], typer.Option(help="Path to the destination tfstate file")] = None,
    sourceState: Annotated[Optional[Path], typer.Option(help="Path to the source tfstate file")] = None,
    #dryrun: Annotated[bool, typer.Option(help="dry run.")] = False,
):
    coreCheck = utility.checkFile(destinationState, "tfstate")
    componentsCheck = utility.checkFile(sourceState, "tfstate")

    if coreCheck == componentsCheck == True:
        migrateResources(module, destinationState, sourceState)

def migrateResources(module: str, destinationState, sourceState):
    moduleName = "module." + module
    moduleState = getModuleState(sourceState, moduleName)

    coreState = mergeModuleState(destinationState, moduleState, module)
    utility.saveState("core", coreState)

    componentsState = deleteModuleState(sourceState, moduleName)
    utility.saveState("components", componentsState)

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

if __name__ == "__main__":
    typer.run(main)
