Contributions welcome!  

Here's just some random notes on the development process. 

## Setup
1. `pip install pipenv`
1. `pipenv install --dev`


## Testing
1. Run tests: `pipenv run test`
1. Run pylint: `pylint UnleashClient`
1. Run mypy: `mypy UnleashCLient`

It's good to run static analysis locally, otherwise CI build will fail!

## Release
Land all your PRs. :)
1. Update changelog.md
1. `mkdocs gh-deploy`
1. `bumpversion [major/minor/patch]`
1. `make build`