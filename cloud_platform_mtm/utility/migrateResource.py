import re
import typer

def validateResourceName(resource: str):
    match = re.search(r'\w*\.\S\w*', resource)

    if match:
        return True
    else:
        print("Resource does not match expected pattern - resource_type.resource_name")
        raise typer.Exit(code=1)