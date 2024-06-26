import typer

def check_file(file, type: str):
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

def save_state(directory: str, state):
    print(f"Saving new state file - {directory}New.tfstate")

    file_name = directory + "New.tfstate"

    with open(file_name, "w") as text_file:
        text_file.write(state)

def remove_dependencies(resource, name: str):
    for instances in resource:
        if "instances" in instances:
            for instance in resource['instances']:
                if "dependencies" in instance:
                    if any(name in s for s in instance['dependencies']):
                        new_dependencies = [x for x in instance['dependencies'] if name not in x]
                        instance.pop("dependencies")
                        instance["dependencies"] = new_dependencies

    return(resource)