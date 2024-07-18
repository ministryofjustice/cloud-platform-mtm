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

Commits should follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) standard. When branches are merged a release PR is either created or updated with relevant commit history. Merging this PR in will create a new release.

## Install

Grab the wheel from releases and:

`pip install --user package.whl`

## Running

```
mtm --help
```

Migrate a module:

```
mtm migrate-module cert_manager $source $destination
```

Migrate a resource:

```
mtm migrate-module kubectl_manifest.prometheus_operator_crds $source $destination
```

Migrate a resource from a module:

```
mtm migrate-module kubectl_manifest.prometheus_operator_crds --remove-module $source $destination
```