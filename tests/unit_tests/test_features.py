import pytest
from UnleashClient.features import Feature
from UnleashClient.strategies import RemoteAddress, UserWithId, Default
from UnleashClient.variants import Variants
from tests.utilities import generate_email_list
from tests.utilities.testing_constants import IP_LIST
from tests.utilities.mocks.mock_variants import VARIANTS


(EMAIL_LIST, CONTEXT) = generate_email_list(20)


@pytest.fixture()
def test_feature():
    strategies = [RemoteAddress(parameters={"IPs": IP_LIST}), UserWithId(parameters={"userIds": EMAIL_LIST})]
    yield Feature("My Feature", True, strategies)


@pytest.fixture()
def test_feature_variants():
    strategies = [Default()]
    variants = Variants(VARIANTS, "My Feature")
    yield Feature("My Feature", True, strategies, variants)


def test_create_feature_true(test_feature):
    my_feature = test_feature

    CONTEXT["remoteAddress"] = "69.208.0.1"
    assert my_feature.is_enabled(CONTEXT)
    assert my_feature.yes_count == 1

    my_feature.reset_stats()
    assert my_feature.yes_count == 0
    assert not my_feature.impression_data


def test_create_feature_false(test_feature):
    my_feature = test_feature

    CONTEXT["remoteAddress"] = "1.208.0.1"
    CONTEXT["userId"] = "random@random.com"
    assert not my_feature.is_enabled(CONTEXT)
    assert my_feature.no_count == 1

    my_feature.reset_stats()
    assert my_feature.no_count == 0


def test_create_feature_not_enabled(test_feature):
    my_feature = test_feature
    my_feature.enabled = False

    CONTEXT["remoteAddress"] = "69.208.0.1"
    assert not my_feature.is_enabled(CONTEXT)


def test_create_feature_exception(test_feature):
    strategies = [{}, UserWithId(parameters={"userIds": EMAIL_LIST})]
    my_feature = Feature("My Feature", True, strategies)

    CONTEXT["remoteAddress"] = "69.208.0.1"
    assert not my_feature.is_enabled(CONTEXT)


def test_select_variation_novariation(test_feature):
    selected_variant = test_feature.get_variant()
    assert type(selected_variant) == dict
    assert selected_variant['name'] == 'disabled'


def test_select_variation_variation(test_feature_variants):
    selected_variant = test_feature_variants.get_variant({'userId': '2'})
    assert selected_variant['enabled']
    assert selected_variant['name'] == 'VarB'
