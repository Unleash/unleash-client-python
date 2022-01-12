****************************************
Development
****************************************

Contributions welcome!  

Here are some notes about common tools and tasks you'll run into when working on `unleash-client-python`.

Testing
#######################################

1. Activate your virtualenv solution (e.g. `source activate ucp`).
2. Run linting & tests: `make test`

Release
#######################################

1. Land all your PRs on `main`. :)
2. Update changelog.md and other sundry documentation.
3. Create tag on master branch.
4. Deploy documents by running `mkdocs gh-deploy`
5. Create new Release in Github and paste in Changelog.
6. Github Actions workflow will automagically publish to Pypi. ^^