Contributions welcome!  

Here's just some random notes on the development process. 

## Setup
1. `pip install pipenv`
2. `pipenv --python 3.7`
3. `pipenv install --dev`


## Testing
1. Activate your pipenv:  `pipenv shell`
1. Run linting & tests: `make test`

## Release
Land all your PRs. :)
1. Update changelog.md
2. `mkdocs gh-deploy`
3. `bumpversion [major/minor/patch]`
4. `make build`