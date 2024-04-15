import typer

from typing_extensions import Annotated
from pathlib import Path
from cloud_platform_mtm.utility import utility, source, destination


app = typer.Typer()

@app.callback()
def callback():
    """
    Migrate terraform modules
    """

@app.command()
def migrate(
    module: Annotated[str, typer.Argument(help="Module to migrate")],
    source_path: Annotated[Path, typer.Argument(help="Path to source tfstate file")],
    destination_path: Annotated[Path, typer.Argument(help="Path to destination tfstate file")]
    ):
    """
    Migrate terraform modules
    """
    destinationCheck = utility.checkFile(destination_path, "tfstate")
    sourceCheck = utility.checkFile(source_path, "tfstate")

    if destinationCheck == sourceCheck == True:
        migrateResources(module, destination_path, source_path)

def migrateResources(module: str, destinationState, sourceState):
    moduleName = "module." + module
    moduleState = destination.getModuleState(sourceState, moduleName)

    destinationNewState = destination.mergeModuleState(destinationState, moduleState, module)
    utility.saveState("core", destinationNewState)

    sourceNewState = source.deleteModuleState(sourceState, moduleName)
    utility.saveState("components", sourceNewState)

if __name__ == "__main__":
    app()