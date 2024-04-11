import typer

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