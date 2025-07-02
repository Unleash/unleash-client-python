## Developing

For development, you'll need to setup the environment to run the tests. This repository is using
tox to run the test suite to test against multiple versions of Python. Running the tests is as simple as running this command in the makefile:

```
tox -e py311
```

This command will take care of downloading the client specifications and putting them in the correct place in the repository, and install all the dependencies you need.

However, there are some caveats to this method. There is no easy way to run a single test, and running the entire test suite can be slow.

### Manual setup

First, make sure you have pip or pip3 installed.

Then set up your virtual environment:

Linux & Mac:

```
python3 -m venv venv
source venv/bin/activate
```

Windows + cmd:

```
python -m venv venv
venv\Scripts\activate.bat
```

Powershell:

```
python -m venv venv
venv\Scripts\activate.bat
```

Once you've done your setup, run:
```
pip install -r requirements.txt
```

Run the get-spec script to download the client specifications tests:
```
./scripts/get-spec.sh
```

Now you can run the tests by running `pytest` in the root directory.

In order to run a single test, run the following command:

```
pytest testfile.py::function_name

# example: pytest tests/unit_tests/test_client.py::test_consistent_results
```

### Linting

In order to lint all the files you can run the following command:

```
make fmt
```
