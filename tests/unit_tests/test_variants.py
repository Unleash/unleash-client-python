import pytest
from UnleashClient.variants import Variants


VARIANTS = \
    [
        {
            "name": "VarA",
            "weight": 34,
            "payload": {
                "type": "string",
                "value": "Test1"
            },
            "overrides": [
                {
                    "contextName": "userId",
                    "values": [
                        "ivanklee86@gmail.com"
                    ]
                }
            ]
        },
        {
            "name": "VarB",
            "weight": 33,
            "payload": {
                "type": "string",
                "value": "Test 2"
            }
        },
        {
            "name": "VarC",
            "weight": 33,
            "payload": {
                "type": "string",
                "value": "Test 3"
            }
        }
    ]


@pytest.fixture()
def variations():
    yield Variants(VARIANTS)


def test_variations_overridematch(variations):
    override_variant = variations._apply_overrides({'userId': 'ivanklee86@gmail.com'})
    assert override_variant['name'] == 'VarA'


def test_variations_overridnoematch(variations):
    assert not variations._apply_overrides({'userId': 'ivanklee87@gmail.com'})
