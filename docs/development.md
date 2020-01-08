Contributions welcome!  

Here are some notes about common tools and tasks you'll run into when working on `unleash-client-python`.

## Tools
* [miniconda](https://docs.conda.io/en/latest/miniconda.html) - Used for local tox-ing to minimize friction when developing on a Mac. =)

## Setup
1. Create a new conda environment (`conda create -n ucp python=3.7`) or a venv.
2. Install packages: `pip install requirements-local.txt`.
3. If using Pycharm, add [conda env](https://medium.com/infinity-aka-aseem/how-to-setup-pycharm-with-an-anaconda-virtual-environment-already-created-fb927bacbe61) as your project interpreter.

## Testing
1. Activate your virtualenv solution (e.g. `source activate ucp`).
1. Run linting & tests: `make test`
1. Run tox tests `make tox-osx`

## Dependency management
* Adding
    * Add version-less package to `requirement-*.txt`file (in case we ever just wanna install everything) and versioned package to `requirements.txt`.
* Updating
    * Use [pur](https://github.com/alanhamlett/pip-update-requirements) to update requirements.txt.
    * If updating package requirements, update the `setup.py` file.

## mmh3 on OSX
If having trouble installing mmh3 on OSX, try:
```shell
CFLAGS="-mmacosx-version-min=10.13" pip install mmh3
```

## Release
1. Land all your PRs on `master`. :)
1. Update changelog.md and other sundry documentation.
1. Deploy documents by running `mkdocs gh-deploy`
1. Run `bumpversion [major/minor/patch]` to generate new version & tag.
1. Push tag to remotes.
1. Create new Release in Github and paste in Changelog.
1. Github Actions workflow will automagically publish to Pypi. ^^