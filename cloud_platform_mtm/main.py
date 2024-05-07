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
    destination_check = utility.check_file(destination_path, "tfstate")
    source_check = utility.check_file(source_path, "tfstate")

    if destination_check and source_check:
        migrateModule.migrate_module_resources(module, destination_path, source_path)

@app.command()
def migrate_resource(
    resource: Annotated[str, typer.Argument(help="Resource to migrate")],
    source_path: Annotated[Path, typer.Argument(help="Path to source tfstate file")],
    destination_path: Annotated[Path, typer.Argument(help="Path to destination tfstate file")]
    ):
    """
    Migrate terraform resource
    """
    destination_check = utility.check_file(destination_path, "tfstate")
    source_check = utility.check_file(source_path, "tfstate")

    if destination_check and source_check and migrateResource.validate_resource_name(resource):
        migrateResource.migrate_resource(resource, destination_path, source_path)

if __name__ == "__main__":
    app()