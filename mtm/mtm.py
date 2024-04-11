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
    destinationCheck = utility.checkFile(destinationState, "tfstate")
    sourceCheck = utility.checkFile(sourceState, "tfstate")

    if destinationCheck == sourceCheck == True:
        migrateResources(module, destinationState, sourceState)

def migrateResources(module: str, destinationState, sourceState):
    moduleName = "module." + module
    moduleState = destination.getModuleState(sourceState, moduleName)

    destinationNewState = destination.mergeModuleState(destinationState, moduleState, module)
    utility.saveState("core", destinationNewState)

    sourceNewState = source.deleteModuleState(sourceState, moduleName)
    utility.saveState("components", sourceNewState)

if __name__ == "__main__":
    typer.run(main)
