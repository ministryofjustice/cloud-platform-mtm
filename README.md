# Move terraform modules - MTM

A Python script to move terraform modules between two state files.

> WARNING: Here be dragons. Moving terraform state like this is not advised!

## Requirements

* [pipx](https://github.com/pypa/pipx)
* [poetry](https://python-poetry.org/docs/#installation)

We use `pipx` to install `poetry` which then manages the packages dependencies.

## Development

```
poetry install
```

## Install

Grab the wheel from releases and:

`pip install --user package.whl`

## Running

```
mtm --help
```
