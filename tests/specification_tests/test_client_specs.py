import json
import uuid
from os import path
from UnleashClient import UnleashClient
from tests.utilities.testing_constants import URL, APP_NAME
from UnleashClient.cache import FileCache
import pytest


CLIENT_SPEC_PATH = "tests/specification_tests/client-specification/specifications"


def load_spec(spec):
    with open(path.join(CLIENT_SPEC_PATH, spec)) as _f:
        data = json.load(_f)
        return (
            data["name"],
            data["state"],
            data.get("tests") or [],
            data.get("variantTests") or [],
        )


def load_specs():
    with open(path.join(CLIENT_SPEC_PATH, "index.json")) as _f:
        return json.load(_f)


def iter_spec():
    for spec in load_specs():
        name, state, tests, variant_tests = load_spec(spec)

        cache = FileCache("MOCK_CACHE")
        cache.bootstrap_from_dict(state)

        unleash_client = UnleashClient(
            url=URL,
            app_name=APP_NAME,
            instance_id="pytest_%s" % uuid.uuid4(),
            disable_metrics=True,
            disable_registration=True,
            cache=cache,
        )

        unleash_client.initialize_client(fetch_toggles=False)

        for test in tests:
            yield name, test["description"], unleash_client, test, False

        for variant_test in variant_tests:
            yield name, test["description"], unleash_client, variant_test, True

        unleash_client.destroy()


try:
    ALL_SPECS = list(iter_spec())
    TEST_DATA = [x[2:] for x in ALL_SPECS]
    TEST_NAMES = [f"{x[0]}-{x[1]}" for x in ALL_SPECS]
except FileNotFoundError:
    print(
        "Cannot find the client specifications, these can be downloaded with the following command: 'git clone --depth 5 --branch v4.2.2 https://github.com/Unleash/client-specification.git tests/specification_tests/client-specification'"
    )
    raise


@pytest.mark.parametrize("spec", TEST_DATA, ids=TEST_NAMES)
def test_spec(spec):
    unleash_client, test_data, is_variant_test = spec
    if not is_variant_test:
        toggle_name = test_data["toggleName"]
        expected = test_data["expectedResult"]
        context = test_data.get("context")
        assert unleash_client.is_enabled(toggle_name, context) == expected
    else:
        toggle_name = test_data["toggleName"]
        expected = test_data["expectedResult"]
        context = test_data.get("context")

        variant = unleash_client.get_variant(toggle_name, context)
        assert variant == expected
