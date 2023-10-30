import pytest

from tests.utilities.mocks.mock_variants import VARIANTS, VARIANTS_WITH_STICKINESS
from UnleashClient.variants import Variants


@pytest.fixture()
def variations():
    yield Variants(VARIANTS, "TestFeature")


@pytest.fixture()
def variations_with_stickiness():
    yield Variants(VARIANTS_WITH_STICKINESS, "TestFeature")


def test_variations_override_match(variations):
    override_variant = variations._apply_overrides({"userId": "1"})
    assert override_variant["name"] == "VarA"


def test_variations_overrid_nomatch(variations):
    assert not variations._apply_overrides({"userId": "2"})


def test_variations_seed(variations):
    # Random seed generation
    context = {}
    seed = variations._get_seed(context)
    assert float(seed) > 0

    # UserId, SessionId, and remoteAddress
    context = {"userId": "1", "sessionId": "1", "remoteAddress": "1.1.1.1"}

    assert context["userId"] == variations._get_seed(context)
    del context["userId"]
    assert context["sessionId"] == variations._get_seed(context)
    del context["sessionId"]
    assert context["remoteAddress"] == variations._get_seed(context)


def test_variations_seed_override(variations):
    # UserId, SessionId, and remoteAddress
    context = {
        "userId": "1",
        "sessionId": "1",
        "remoteAddress": "1.1.1.1",
        "customField": "ActuallyAmAHamster",
    }

    assert context["customField"] == variations._get_seed(context, "customField")


def test_variation_selectvariation_happypath(variations):
    variant = variations.get_variant({"userId": "2"})
    assert variant
    assert "payload" in variant
    assert variant["name"] == "VarA"


def test_variation_customvariation(variations_with_stickiness):
    variations = variations_with_stickiness
    variant = variations.get_variant({"customField": "ActuallyAmAHamster1234"})
    assert variant
    assert "payload" in variant
    assert variant["name"] == "VarC"


def test_variation_selectvariation_multi(variations):
    tracker = {}
    for x in range(100):
        variant = variations.get_variant({})
        name = variant["name"]
        if name in tracker:
            tracker[name] += 1
        else:
            tracker[name] = 1

    assert len(tracker) == 3
    assert sum([tracker[x] for x in tracker.keys()]) == 100


def test_variation_override(variations):
    variant = variations.get_variant({"userId": "1"})
    assert variant
    assert "payload" in variant
    assert variant["name"] == "VarA"


def test_variation_novariants():
    variations = Variants([], "TestFeature")
    variant = variations.get_variant({})
    assert variant
    assert variant["name"] == "disabled"
