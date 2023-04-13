from datetime import datetime

import pytest
import pytz

from tests.utilities.mocks import mock_constraints
from UnleashClient.constraints import Constraint


@pytest.fixture()
def constraint_IN():
    yield Constraint(mock_constraints.CONSTRAINT_DICT_IN)


@pytest.fixture()
def constraint_NOTIN():
    yield Constraint(mock_constraints.CONSTRAINT_DICT_NOTIN)


def test_constraint_IN_match(constraint_IN):
    constraint = constraint_IN
    context = {"appName": "test"}

    assert constraint.apply(context)


def test_constraint_IN_not_match(constraint_IN):
    constraint = constraint_IN
    context = {"appName": "test3"}

    assert not constraint.apply(context)


def test_constraint_IN_missingcontext(constraint_IN):
    constraint = constraint_IN
    assert not constraint.apply({})


def test_constraint_NOTIN_missingcontext(constraint_NOTIN):
    constraint = constraint_NOTIN
    assert constraint.apply({})


def test_constraint_NOTIN_missingcontext_inversion():
    constraint = Constraint(mock_constraints.CONSTRAINT_DICT_NOTIN_INVERT)
    assert not constraint.apply({})


def test_constraint_NOTIN_match(constraint_NOTIN):
    constraint = constraint_NOTIN
    context = {"appName": "test"}

    assert not constraint.apply(context)


def test_constraint_NOTIN_not_match(constraint_NOTIN):
    constraint = constraint_NOTIN
    context = {"appName": "test3"}

    assert constraint.apply(context)


def test_constraint_inversion():
    constraint_ci = Constraint(
        constraint_dict=mock_constraints.CONSTRAINT_DICT_STR_INVERT
    )

    assert not constraint_ci.apply({"customField": "adogb"})


def test_constraint_STR_CONTAINS():
    constraint_not_ci = Constraint(
        constraint_dict=mock_constraints.CONSTRAINT_DICT_STR_CONTAINS_NOT_CI
    )
    constraint_ci = Constraint(
        constraint_dict=mock_constraints.CONSTRAINT_DICT_STR_CONTAINS_CI
    )

    assert constraint_ci.apply({"customField": "adogb"})
    assert not constraint_ci.apply({"customField": "aparrotb"})
    assert constraint_ci.apply({"customField": "ahamsterb"})

    assert constraint_not_ci.apply({"customField": "adogb"})
    assert not constraint_ci.apply({"customField": "aparrotb"})
    assert not constraint_not_ci.apply({"customField": "ahamsterb"})


def test_constraint_STR_ENDS_WITH():
    constraint_not_ci = Constraint(
        constraint_dict=mock_constraints.CONSTRAINT_DICT_STR_ENDS_WITH_NOT_CI
    )
    constraint_ci = Constraint(
        constraint_dict=mock_constraints.CONSTRAINT_DICT_STR_ENDS_WITH_CI
    )

    assert constraint_ci.apply({"customField": "adog"})
    assert not constraint_ci.apply({"customField": "aparrot"})
    assert constraint_ci.apply({"customField": "ahamster"})

    assert constraint_not_ci.apply({"customField": "adog"})
    assert not constraint_not_ci.apply({"customField": "aparrot"})
    assert not constraint_not_ci.apply({"customField": "ahamster"})


def test_constraint_STR_STARTS_WITH():
    constraint_not_ci = Constraint(
        constraint_dict=mock_constraints.CONSTRAINT_DICT_STR_STARTS_WITH_NOT_CI
    )
    constraint_ci = Constraint(
        constraint_dict=mock_constraints.CONSTRAINT_DICT_STR_STARTS_WITH_CI
    )

    assert constraint_ci.apply({"customField": "dogb"})
    assert not constraint_ci.apply({"customField": "parrotb"})
    assert constraint_ci.apply({"customField": "hamsterb"})

    assert constraint_not_ci.apply({"customField": "dogb"})
    assert not constraint_not_ci.apply({"customField": "parrotb"})
    assert not constraint_not_ci.apply({"customField": "hamsterb"})


def test_constraints_NUM_EQ():
    constraint = Constraint(constraint_dict=mock_constraints.CONSTRAINT_NUM_EQ)

    assert not constraint.apply({"customField": 4})
    assert constraint.apply({"customField": 5})
    assert not constraint.apply({"customField": 6})


def test_constraints_NUM_GT():
    constraint = Constraint(constraint_dict=mock_constraints.CONSTRAINT_NUM_GT)

    assert not constraint.apply({"customField": 4})
    assert not constraint.apply({"customField": 5})
    assert constraint.apply({"customField": 6})


def test_constraints_NUM_GTE():
    constraint = Constraint(constraint_dict=mock_constraints.CONSTRAINT_NUM_GTE)

    assert not constraint.apply({"customField": 4})
    assert constraint.apply({"customField": 5})
    assert constraint.apply({"customField": 6})


def test_constraints_NUM_LT():
    constraint = Constraint(constraint_dict=mock_constraints.CONSTRAINT_NUM_LT)

    assert constraint.apply({"customField": 4})
    assert not constraint.apply({"customField": 5})
    assert not constraint.apply({"customField": 6})


def test_constraints_NUM_LTE():
    constraint = Constraint(constraint_dict=mock_constraints.CONSTRAINT_NUM_LTE)

    assert constraint.apply({"customField": 4})
    assert constraint.apply({"customField": 5})
    assert not constraint.apply({"customField": 6})


def test_constraints_NUM_FLOAT():
    constraint = Constraint(constraint_dict=mock_constraints.CONSTRAINT_NUM_FLOAT)

    assert constraint.apply({"customField": 5})
    assert constraint.apply({"customField": 5.1})
    assert not constraint.apply({"customField": 5.2})


def test_constraints_DATE_AFTER():
    constraint = Constraint(constraint_dict=mock_constraints.CONSTRAINT_DATE_AFTER)

    assert constraint.apply({"currentTime": datetime(2022, 1, 23, tzinfo=pytz.UTC)})
    assert not constraint.apply({"currentTime": datetime(2022, 1, 22, tzinfo=pytz.UTC)})
    assert not constraint.apply({"currentTime": datetime(2022, 1, 21, tzinfo=pytz.UTC)})


def test_constraints_DATE_BEFORE():
    constraint = Constraint(constraint_dict=mock_constraints.CONSTRAINT_DATE_BEFORE)

    assert not constraint.apply({"currentTime": datetime(2022, 1, 23, tzinfo=pytz.UTC)})
    assert not constraint.apply({"currentTime": datetime(2022, 1, 22, tzinfo=pytz.UTC)})
    assert constraint.apply({"currentTime": datetime(2022, 1, 21, tzinfo=pytz.UTC)})


def test_constraints_default():
    constraint = Constraint(constraint_dict=mock_constraints.CONSTRAINT_DATE_BEFORE)

    assert not constraint.apply({})


def test_constraints_date_error():
    constraint = Constraint(constraint_dict=mock_constraints.CONSTRAINT_DATE_ERROR)
    assert not constraint.apply({"currentTime": datetime(2022, 1, 23)})


def test_constraints_SEMVER_EQ():
    constraint = Constraint(constraint_dict=mock_constraints.CONSTRAINT_SEMVER_EQ)

    assert not constraint.apply({"customField": "1.2.1"})
    assert constraint.apply({"customField": "1.2.2"})
    assert not constraint.apply({"customField": "1.2.3"})


def test_constraints_SEMVER_GT():
    constraint = Constraint(constraint_dict=mock_constraints.CONSTRAINT_SEMVER_GT)

    assert not constraint.apply({"customField": "1.2.1"})
    assert not constraint.apply({"customField": "1.2.2"})
    assert constraint.apply({"customField": "1.2.3"})


def test_constraints_SEMVER_LT():
    constraint = Constraint(constraint_dict=mock_constraints.CONSTRAINT_SEMVER_LT)

    assert constraint.apply({"customField": "1.2.1"})
    assert not constraint.apply({"customField": "1.2.2"})
    assert not constraint.apply({"customField": "1.2.3"})


def test_constraints_semverexception():
    constraint = Constraint(constraint_dict=mock_constraints.CONSTRAINT_SEMVER_EQ)

    assert not constraint.apply({"customField": "hamstershamsterhamsters"})
