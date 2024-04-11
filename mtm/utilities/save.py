def saveState(module: str, state):
    print(f"Saving new state file - {module}New.tfstate")

    fileName = module + "New.tfstate"

    with open(fileName, "w") as text_file:
        text_file.write(state)