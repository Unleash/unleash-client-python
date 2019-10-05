import pytest
from UnleashClient.strategies.constraints.constraint_schema import ConstraintSchema


CONSTRAINT_DICT_IN = \
    {
        "contextName": "appName",
        "operator": "IN",
        "values": [
            "test",
            "test2"
        ]
    }


CONSTRAINT_DICT_NOTIN = \
    {
        "contextName": "appName",
        "operator": "NOT_IN",
        "values": [
            "test",
            "test2"
        ]
    }


@pytest.fixture()
def constraint_IN():
    schema = ConstraintSchema()
    yield schema.load(CONSTRAINT_DICT_IN)


@pytest.fixture()
def constraint_NOTIN():
    schema = ConstraintSchema()
    yield schema.load(CONSTRAINT_DICT_NOTIN)


def test_constraint_IN_match(constraint_IN):
    constraint = constraint_IN
    context = {
        'appName': 'test'
    }

    assert constraint(context)


def test_constraint_IN_not_match(constraint_IN):
    constraint = constraint_IN
    context = {
        'appName': 'test3'
    }

    assert not constraint(context)


def test_constraint_IN_missingcontext(constraint_IN):
    constraint = constraint_IN
    assert not constraint({})


def test_constraint_NOTIN_match(constraint_NOTIN):
    constraint = constraint_NOTIN
    context = {
        'appName': 'test'
    }

    assert not constraint(context)


def test_constraint_NOTIN_not_match(constraint_NOTIN):
    constraint = constraint_NOTIN
    context = {
        'appName': 'test3'
    }

    assert constraint(context)
