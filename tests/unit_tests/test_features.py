from UnleashClient.features import Feature
from UnleashClient.strategies import RemoteAddress, UserWithId
from tests.utilities import generate_email_list
from tests.utilities.testing_constants import IP_LIST


(EMAIL_LIST, CONTEXT) = generate_email_list(20)


def test_create_feature_true():
    strategies = [RemoteAddress(parameters={"IPs": IP_LIST}), UserWithId(parameters={"userIds": EMAIL_LIST})]
    my_feature = Feature("My Feature", True, strategies)

    CONTEXT["remoteAddress"] = "69.208.0.1"
    assert my_feature.is_enabled(CONTEXT)
    assert my_feature.yes_count == 1

    my_feature.reset_stats()
    assert my_feature.yes_count == 0


def test_create_feature_false():
    strategies = [RemoteAddress(parameters={"IPs": IP_LIST}), UserWithId(parameters={"userIds": EMAIL_LIST})]
    my_feature = Feature("My Feature", True, strategies)

    CONTEXT["remoteAddress"] = "1.208.0.1"
    CONTEXT["userId"] = "random@random.com"
    assert not my_feature.is_enabled(CONTEXT)
    assert my_feature.no_count == 1

    my_feature.reset_stats()
    assert my_feature.no_count == 0
