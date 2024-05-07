import typer

from typing_extensions import Annotated
from pathlib import Path
from cloud_platform_mtm.utility import utility, migrateModule, migrateResource


app = typer.Typer()

@app.callback()
def callback():
    """
    Migrate terraform modules
    """

@app.command()
def migrate_module(
    module: Annotated[str, typer.Argument(help="Module to migrate")],
    source_path: Annotated[Path, typer.Argument(help="Path to source tfstate file")],
    destination_path: Annotated[Path, typer.Argument(help="Path to destination tfstate file")]
    ):
    """
    Migrate terraform modules
    """
    destinationCheck = utility.checkFile(destination_path, "tfstate")
    sourceCheck = utility.checkFile(source_path, "tfstate")

    if destinationCheck and sourceCheck:
        migrateModule.migrateModuleResources(module, destination_path, source_path)

@app.command()
def migrate_resource(
    resource: Annotated[str, typer.Argument(help="Resource to migrate")],
    source_path: Annotated[Path, typer.Argument(help="Path to source tfstate file")],
    destination_path: Annotated[Path, typer.Argument(help="Path to destination tfstate file")]
    ):
    """
    Migrate terraform resource
    """
    destinationCheck = utility.checkFile(destination_path, "tfstate")
    sourceCheck = utility.checkFile(source_path, "tfstate")

    if destinationCheck and sourceCheck and migrateResource.validate_resource_name(resource):
        migrateResource.migrate_resource(resource, destination_path, source_path)

if __name__ == "__main__":
    app()