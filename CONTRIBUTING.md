# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.

Please note we have a code of conduct, please follow it in all your interactions with the project.

## Setup
To setup the development environment you'll need some additional modules:

    pip install jsonschema pytest flake8

Then in the repo install the module using:

    pip install -e .

Optional, configure a proxy:

    $ HTTP_PROXY="127.0.0.1:8000"

## Testing

To validate your pull request, your changes have to pass tests:
- Run `flake8` to ensure there are no lint errors.
- Run unittest (`pytest -m MARKERS`).

> WARNING: Do not run `pytest` without arguments, always use [markers](https://docs.pytest.org/en/6.2.x/example/markers.html) with the `-m` argument.
> You can find defined markers in [this file](./pytest.ini).

## Submitting Changes

Prefer atomic commits (one feature per commit).

Always write a clear log message for your commits. One-line messages are fine for small changes, but bigger changes should look like this:

    $ git commit -m "A brief summary of the commit
    >
    > A paragraph describing what changed and its impact."

