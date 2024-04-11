#!/usr/bin/env python3

from pathlib import Path
from typing import Optional

import typer

from typing_extensions import Annotated
from utility import utility, source, destination

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
    moduleState = source.getModuleState(sourceState, moduleName)

    coreState = source.mergeModuleState(destinationState, moduleState, module)
    utility.saveState("core", coreState)

    componentsState = destination.deleteModuleState(sourceState, moduleName)
    utility.saveState("components", componentsState)

if __name__ == "__main__":
    typer.run(main)
