import pytest
from UnleashClient.constraints import Constraint
from tests.utilities.mocks import mock_constraints


@pytest.fixture()
def constraint_IN():
    yield Constraint(mock_constraints.CONSTRAINT_DICT_IN)


@pytest.fixture()
def constraint_NOTIN():
    yield Constraint(mock_constraints.CONSTRAINT_DICT_NOTIN)



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


def test_constraint_STR_ENDS_WITH_not_insensitive():
    constraint_case_insensitive = Constraint(constraint_dict=mock_constraints.CONSTRAINT_DICT_STR_ENDS_WITH)

    assert constraint_case_insensitive.apply({'customField': "dot"})
    assert not constraint_case_insensitive.apply({'customField': "hamster"})
