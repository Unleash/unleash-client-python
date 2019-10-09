import pytest
from UnleashClient.constraints import Constraint


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
    yield Constraint(CONSTRAINT_DICT_IN)


@pytest.fixture()
def constraint_NOTIN():
    yield Constraint(CONSTRAINT_DICT_NOTIN)


def test_constraint_IN_match(constraint_IN):
    constraint = constraint_IN
    context = {
        'appName': 'test'
    }

    assert constraint.apply(context)


def test_constraint_IN_not_match(constraint_IN):
    constraint = constraint_IN
    context = {
        'appName': 'test3'
    }

    assert not constraint.apply(context)


def test_constraint_IN_missingcontext(constraint_IN):
    constraint = constraint_IN
    assert not constraint.apply({})


def test_constraint_NOTIN_match(constraint_NOTIN):
    constraint = constraint_NOTIN
    context = {
        'appName': 'test'
    }

    assert not constraint.apply(context)


def test_constraint_NOTIN_not_match(constraint_NOTIN):
    constraint = constraint_NOTIN
    context = {
        'appName': 'test3'
    }

    assert constraint.apply(context)
