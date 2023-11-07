import json
import time
import warnings
from pathlib import Path

import pytest
import responses
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from blinker import signal

from tests.utilities.mocks.mock_all_features import MOCK_ALL_FEATURES
from tests.utilities.mocks.mock_features import (
    MOCK_FEATURE_ENABLED_NO_VARIANTS_RESPONSE,
    MOCK_FEATURE_RESPONSE,
    MOCK_FEATURE_RESPONSE_PROJECT,
    MOCK_FEATURE_WITH_DEPENDENCIES_RESPONSE,
)
from tests.utilities.testing_constants import (
    APP_NAME,
    CUSTOM_HEADERS,
    CUSTOM_OPTIONS,
    DISABLE_METRICS,
    DISABLE_REGISTRATION,
    ENVIRONMENT,
    ETAG_VALUE,
    INSTANCE_ID,
    METRICS_INTERVAL,
    METRICS_JITTER,
    PROJECT_NAME,
    PROJECT_URL,
    REFRESH_INTERVAL,
    REFRESH_JITTER,
    URL,
)
from UnleashClient import INSTANCES, UnleashClient
from UnleashClient.cache import FileCache
from UnleashClient.constants import FEATURES_URL, METRICS_URL, REGISTER_URL
from UnleashClient.events import UnleashEvent, UnleashEventType
from UnleashClient.strategies import Strategy
from UnleashClient.utils import InstanceAllowType


class EnvironmentStrategy(Strategy):
    def load_provisioning(self) -> list:
        return [x.strip() for x in self.parameters["environments"].split(",")]

    def apply(self, context: dict = None) -> bool:
        """
        Turn on if environemnt is a match.

        :return:
        """
        default_value = False

        if "environment" in context.keys():
            default_value = context["environment"] in self.parsed_provisioning

        return default_value


@pytest.fixture(autouse=True)
def before_each():
    INSTANCES._reset()


@pytest.fixture
def cache(tmpdir):
    return FileCache(APP_NAME, directory=tmpdir.dirname)


@pytest.fixture()
def unleash_client(cache):
    unleash_client = UnleashClient(
        URL,
        APP_NAME,
        refresh_interval=REFRESH_INTERVAL,
        metrics_interval=METRICS_INTERVAL,
        cache=cache,
    )
    yield unleash_client
    unleash_client.destroy()


@pytest.fixture()
def unleash_client_project(cache):
    unleash_client = UnleashClient(
        URL,
        APP_NAME,
        refresh_interval=REFRESH_INTERVAL,
        metrics_interval=METRICS_INTERVAL,
        cache=cache,
        project_name=PROJECT_NAME,
    )
    yield unleash_client
    unleash_client.destroy()


@pytest.fixture()
def unleash_client_nodestroy(cache):
    unleash_client = UnleashClient(
        URL,
        APP_NAME,
        refresh_interval=REFRESH_INTERVAL,
        metrics_interval=METRICS_INTERVAL,
        cache=cache,
    )
    yield unleash_client


@pytest.fixture()
def unleash_client_toggle_only(cache):
    unleash_client = UnleashClient(
        URL,
        APP_NAME,
        refresh_interval=REFRESH_INTERVAL,
        metrics_interval=METRICS_INTERVAL,
        disable_registration=True,
        disable_metrics=True,
        cache=cache,
    )
    yield unleash_client
    unleash_client.destroy()


@pytest.fixture()
def unleash_client_bootstrap_dependencies():
    cache = FileCache("MOCK_CACHE")
    cache.bootstrap_from_dict(MOCK_FEATURE_WITH_DEPENDENCIES_RESPONSE)
    unleash_client = UnleashClient(
        url=URL,
        app_name=APP_NAME,
        disable_metrics=True,
        disable_registration=True,
        cache=cache,
        environment="default",
    )
    unleash_client.initialize_client(fetch_toggles=False)
    yield unleash_client


def test_UC_initialize_default():
    client = UnleashClient(URL, APP_NAME)
    assert client.unleash_url == URL
    assert client.unleash_app_name == APP_NAME
    assert client.unleash_metrics_interval == 60


def test_UC_initialize_full():
    client = UnleashClient(
        URL,
        APP_NAME,
        ENVIRONMENT,
        INSTANCE_ID,
        REFRESH_INTERVAL,
        REFRESH_JITTER,
        METRICS_INTERVAL,
        METRICS_JITTER,
        DISABLE_METRICS,
        DISABLE_REGISTRATION,
        CUSTOM_HEADERS,
        CUSTOM_OPTIONS,
    )
    assert client.unleash_instance_id == INSTANCE_ID
    assert client.unleash_refresh_interval == REFRESH_INTERVAL
    assert client.unleash_refresh_jitter == REFRESH_JITTER
    assert client.unleash_metrics_interval == METRICS_INTERVAL
    assert client.unleash_metrics_jitter == METRICS_JITTER
    assert client.unleash_disable_metrics == DISABLE_METRICS
    assert client.unleash_disable_registration == DISABLE_REGISTRATION
    assert client.unleash_custom_headers == CUSTOM_HEADERS
    assert client.unleash_custom_options == CUSTOM_OPTIONS


def test_UC_type_violation():
    client = UnleashClient(URL, APP_NAME, refresh_interval="60")
    assert client.unleash_url == URL
    assert client.unleash_app_name == APP_NAME
    assert client.unleash_refresh_interval == "60"


@responses.activate
def test_uc_lifecycle(unleash_client):
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(
        responses.GET,
        URL + FEATURES_URL,
        json=MOCK_FEATURE_RESPONSE,
        status=200,
        headers={"etag": ETAG_VALUE},
    )
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Create Unleash client and check initial load
    unleash_client.initialize_client()
    time.sleep(1)
    assert unleash_client.is_initialized
    assert len(unleash_client.features) >= 4

    # Simulate caching
    responses.add(
        responses.GET,
        URL + FEATURES_URL,
        json={},
        status=304,
        headers={"etag": ETAG_VALUE},
    )
    time.sleep(16)

    # Simulate server provisioning change
    responses.add(
        responses.GET,
        URL + FEATURES_URL,
        json=MOCK_ALL_FEATURES,
        status=200,
        headers={"etag": "W/somethingelse"},
    )
    time.sleep(30)
    assert len(unleash_client.features) >= 9


@responses.activate
def test_uc_is_enabled(unleash_client):
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(
        responses.GET, URL + FEATURES_URL, json=MOCK_FEATURE_RESPONSE, status=200
    )
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Create Unleash client and check initial load
    unleash_client.initialize_client()
    time.sleep(1)
    assert unleash_client.is_enabled("testFlag")


@responses.activate
def test_uc_project(unleash_client_project):
    unleash_client = unleash_client_project

    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(
        responses.GET, PROJECT_URL, json=MOCK_FEATURE_RESPONSE_PROJECT, status=200
    )
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Create Unleash client and check initial load
    unleash_client.initialize_client()
    time.sleep(1)
    assert unleash_client.is_enabled("ivan-project")


@responses.activate
def test_uc_fallbackfunction(unleash_client, mocker):
    def good_fallback(feature_name: str, context: dict) -> bool:
        return True

    def bad_fallback(feature_name: str, context: dict) -> bool:
        return False

    def context_fallback(feature_name: str, context: dict) -> bool:
        return context["wat"]

    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(
        responses.GET, URL + FEATURES_URL, json=MOCK_FEATURE_RESPONSE, status=200
    )
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)
    fallback_spy = mocker.Mock(wraps=good_fallback)

    # Create Unleash client and check initial load
    unleash_client.initialize_client()
    time.sleep(1)
    # Non-existent feature flag, fallback_function
    assert unleash_client.is_enabled("notFoundTestFlag", fallback_function=fallback_spy)
    assert fallback_spy.call_count == 1
    fallback_spy.reset_mock()

    # Non-existent feature flag, default value, fallback_function
    assert not unleash_client.is_enabled(
        "notFoundTestFlag", fallback_function=bad_fallback
    )
    assert fallback_spy.call_count == 0

    # Existent feature flag, fallback_function
    assert unleash_client.is_enabled("testFlag", fallback_function=good_fallback)
    assert fallback_spy.call_count == 0


@responses.activate
def test_uc_dirty_cache(unleash_client_nodestroy):
    unleash_client = unleash_client_nodestroy
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(
        responses.GET, URL + FEATURES_URL, json=MOCK_FEATURE_RESPONSE, status=200
    )
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Create Unleash client and check initial load
    unleash_client.initialize_client()
    time.sleep(5)
    assert unleash_client.is_enabled("testFlag")
    unleash_client.unleash_scheduler.shutdown()

    # Check that everything works if previous cache exists.
    unleash_client.initialize_client()
    time.sleep(5)
    assert unleash_client.is_enabled("testFlag")


@responses.activate
def test_uc_is_enabled_with_context():
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(
        responses.GET, URL + FEATURES_URL, json=MOCK_FEATURE_RESPONSE, status=200
    )
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    custom_strategies_dict = {"custom-context": EnvironmentStrategy}

    unleash_client = UnleashClient(
        URL, APP_NAME, environment="prod", custom_strategies=custom_strategies_dict
    )
    # Create Unleash client and check initial load
    unleash_client.initialize_client()

    time.sleep(1)
    assert unleash_client.is_enabled("testContextFlag")
    unleash_client.destroy()


@responses.activate
def test_uc_is_enabled_error_states(unleash_client):
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(
        responses.GET, URL + FEATURES_URL, json=MOCK_FEATURE_RESPONSE, status=200
    )
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Create Unleash client and check initial load
    unleash_client.initialize_client()
    time.sleep(1)
    assert not unleash_client.is_enabled("ThisFlagDoesn'tExist")
    assert unleash_client.is_enabled(
        "ThisFlagDoesn'tExist", fallback_function=lambda x, y: True
    )


@responses.activate
def test_uc_context_manager(unleash_client_nodestroy):
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(
        responses.GET, URL + FEATURES_URL, json=MOCK_FEATURE_RESPONSE, status=200
    )
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    with unleash_client_nodestroy as unleash_client:
        assert unleash_client.is_initialized


@responses.activate
def test_uc_not_initialized_isenabled():
    unleash_client = UnleashClient(URL, APP_NAME)
    assert not unleash_client.is_enabled("ThisFlagDoesn'tExist")
    assert unleash_client.is_enabled(
        "ThisFlagDoesn'tExist", fallback_function=lambda x, y: True
    )


def test_uc_dependency(unleash_client_bootstrap_dependencies):
    unleash_client = unleash_client_bootstrap_dependencies
    assert unleash_client.is_enabled("Child")
    assert not unleash_client.is_enabled("WithDisabledDependency")
    assert unleash_client.is_enabled("ComplexExample")
    assert not unleash_client.is_enabled("UnlistedDependency")
    assert not unleash_client.is_enabled("TransitiveDependency")


@responses.activate
def test_uc_get_variant():
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(
        responses.GET, URL + FEATURES_URL, json=MOCK_FEATURE_RESPONSE, status=200
    )
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    unleash_client = UnleashClient(URL, APP_NAME)
    # Create Unleash client and check initial load
    unleash_client.initialize_client()

    time.sleep(1)
    # If feature flag is on.
    variant = unleash_client.get_variant("testVariations", context={"userId": "2"})
    assert variant["name"] == "VarA"
    assert variant["enabled"]
    assert variant["feature_enabled"]

    # If feature flag is not.
    variant = unleash_client.get_variant("testVariations", context={"userId": "3"})
    assert variant["name"] == "disabled"
    assert not variant["enabled"]
    assert not variant["feature_enabled"]

    unleash_client.destroy()


@responses.activate
def test_uc_get_variant_feature_enabled_no_variants():
    cache = FileCache("MOCK_CACHE")
    cache.bootstrap_from_dict(MOCK_FEATURE_ENABLED_NO_VARIANTS_RESPONSE)
    unleash_client = UnleashClient(
        url=URL,
        app_name=APP_NAME,
        disable_metrics=True,
        disable_registration=True,
        cache=cache,
        environment="default",
    )
    unleash_client.initialize_client(fetch_toggles=False)

    # If feature is enabled but has no variants, should return disabled variant with feature_enabled=True
    variant = unleash_client.get_variant("EnabledNoVariants")
    assert variant["name"] == "disabled"
    assert not variant["enabled"]
    assert variant["feature_enabled"]

    unleash_client.destroy()


@responses.activate
def test_uc_not_initialized_getvariant():
    unleash_client = UnleashClient(URL, APP_NAME)
    variant = unleash_client.get_variant("ThisFlagDoesn'tExist")
    assert not variant["enabled"]
    assert variant["name"] == "disabled"
    assert not variant["feature_enabled"]


@responses.activate
def test_uc_metrics(unleash_client):
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(
        responses.GET, URL + FEATURES_URL, json=MOCK_FEATURE_RESPONSE, status=200
    )
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Create Unleash client and check initial load
    unleash_client.initialize_client()
    time.sleep(1)
    assert unleash_client.is_enabled("testFlag")

    time.sleep(12)
    request = json.loads(responses.calls[-1].request.body)
    assert request["bucket"]["toggles"]["testFlag"]["yes"] == 1


@responses.activate
def test_uc_registers_metrics_for_nonexistent_features(unleash_client):
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(
        responses.GET, URL + FEATURES_URL, json=MOCK_FEATURE_RESPONSE, status=200
    )
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Create Unleash client and check initial load
    unleash_client.initialize_client()
    time.sleep(1)

    # Check a flag that doesn't exist
    unleash_client.is_enabled("nonexistent-flag")

    # Verify that the metrics are serialized
    time.sleep(12)
    request = json.loads(responses.calls[-1].request.body)
    assert request["bucket"]["toggles"]["nonexistent-flag"]["no"] == 1


@responses.activate
def test_uc_metrics_dependencies(unleash_client):
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(
        responses.GET,
        URL + FEATURES_URL,
        json=MOCK_FEATURE_WITH_DEPENDENCIES_RESPONSE,
        status=200,
    )
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    unleash_client.initialize_client()
    time.sleep(1)
    assert unleash_client.is_enabled("Child")

    time.sleep(12)
    request = json.loads(responses.calls[-1].request.body)
    assert request["bucket"]["toggles"]["Child"]["yes"] == 1
    assert "Parent" not in request["bucket"]["toggles"]


@responses.activate
def test_uc_registers_variant_metrics_for_nonexistent_features(unleash_client):
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(
        responses.GET, URL + FEATURES_URL, json=MOCK_FEATURE_RESPONSE, status=200
    )
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Create Unleash client and check initial load
    unleash_client.initialize_client()
    time.sleep(1)

    # Check a flag that doesn't exist
    unleash_client.get_variant("nonexistent-flag")

    # Verify that the metrics are serialized
    time.sleep(12)
    request = json.loads(responses.calls[-1].request.body)
    assert request["bucket"]["toggles"]["nonexistent-flag"]["no"] == 1
    assert request["bucket"]["toggles"]["nonexistent-flag"]["variants"]["disabled"] == 1


@responses.activate
def test_uc_disabled_registration(unleash_client_toggle_only):
    unleash_client = unleash_client_toggle_only
    # Set up APIs
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=401)
    responses.add(
        responses.GET, URL + FEATURES_URL, json=MOCK_FEATURE_RESPONSE, status=200
    )
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=401)

    unleash_client.initialize_client()
    unleash_client.is_enabled("testFlag")
    time.sleep(20)
    assert unleash_client.is_enabled("testFlag")

    for api_call in responses.calls:
        assert "/api/client/features" in api_call.request.url


@responses.activate
def test_uc_server_error(unleash_client):
    # Verify that Unleash Client will still fall back gracefully if SERVER ANGRY RAWR, and then recover gracefully.
    unleash_client = unleash_client  # noqa
    # Set up APIs
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=401)
    responses.add(responses.GET, URL + FEATURES_URL, status=500)
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=401)

    unleash_client.initialize_client()
    assert not unleash_client.is_enabled("testFlag")

    responses.remove(responses.GET, URL + FEATURES_URL)
    responses.add(
        responses.GET, URL + FEATURES_URL, json=MOCK_FEATURE_RESPONSE, status=200
    )
    time.sleep(20)
    assert unleash_client.is_enabled("testFlag")


def test_uc_with_invalid_url():
    unleash_client = UnleashClient("thisisnotavalidurl", APP_NAME)

    with pytest.raises(ValueError):
        unleash_client.initialize_client()


def test_uc_with_network_error():
    unleash_client = UnleashClient("https://thisisavalidurl.com", APP_NAME)
    unleash_client.initialize_client()

    assert unleash_client.is_enabled


@responses.activate
def test_uc_multiple_initializations(unleash_client):
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(
        responses.GET,
        URL + FEATURES_URL,
        json=MOCK_FEATURE_RESPONSE,
        status=200,
        headers={"etag": ETAG_VALUE},
    )
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Create Unleash client and check initial load
    unleash_client.initialize_client()
    time.sleep(1)
    assert unleash_client.is_initialized
    assert len(unleash_client.features) >= 4

    with warnings.catch_warnings(record=True) as w:
        # Try and initialize client again.
        unleash_client.initialize_client()

    assert len(w) == 1
    assert "initialize" in str(w[0].message)


@responses.activate
def test_uc_cache_bootstrap_dict(cache):
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(
        responses.GET,
        URL + FEATURES_URL,
        json=MOCK_FEATURE_RESPONSE,
        status=200,
        headers={"etag": ETAG_VALUE},
    )
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Set up cache
    cache.bootstrap_from_dict(initial_config=MOCK_FEATURE_RESPONSE_PROJECT)

    # Check bootstrapping
    unleash_client = UnleashClient(
        URL,
        APP_NAME,
        refresh_interval=REFRESH_INTERVAL,
        metrics_interval=METRICS_INTERVAL,
        cache=cache,
    )
    assert len(unleash_client.features) == 1
    assert unleash_client.is_enabled("ivan-project")

    # Create Unleash client and check initial load
    unleash_client.initialize_client()
    time.sleep(1)
    assert unleash_client.is_initialized
    assert len(unleash_client.features) >= 4
    assert unleash_client.is_enabled("testFlag")


@responses.activate
def test_uc_cache_bootstrap_file(cache):
    # Set up cache
    test_file = Path(
        Path(__file__).parent.resolve(),
        "..",
        "utilities",
        "mocks",
        "mock_bootstrap.json",
    )
    cache.bootstrap_from_file(initial_config_file=test_file)

    # Check bootstrapping
    unleash_client = UnleashClient(
        URL,
        APP_NAME,
        refresh_interval=REFRESH_INTERVAL,
        metrics_interval=METRICS_INTERVAL,
        cache=cache,
    )
    assert len(unleash_client.features) >= 1
    assert unleash_client.is_enabled("ivan-project")


@responses.activate
def test_uc_cache_bootstrap_url(cache):
    # Set up API
    responses.add(
        responses.GET,
        URL + FEATURES_URL,
        json=MOCK_FEATURE_RESPONSE,
        status=200,
        headers={"etag": ETAG_VALUE},
    )

    # Set up cache
    cache.bootstrap_from_url(initial_config_url=URL + FEATURES_URL)

    # Check bootstrapping
    unleash_client = UnleashClient(
        URL,
        APP_NAME,
        refresh_interval=REFRESH_INTERVAL,
        metrics_interval=METRICS_INTERVAL,
        cache=cache,
    )
    assert len(unleash_client.features) >= 4
    assert unleash_client.is_enabled("testFlag")


@responses.activate
def test_uc_custom_scheduler():
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(
        responses.GET,
        URL + FEATURES_URL,
        json=MOCK_FEATURE_RESPONSE,
        status=200,
        headers={"etag": ETAG_VALUE},
    )
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Set up UnleashClient
    custom_executors = {"hamster_executor": ThreadPoolExecutor()}

    custom_scheduler = BackgroundScheduler(executors=custom_executors)

    unleash_client = UnleashClient(
        URL,
        APP_NAME,
        refresh_interval=5,
        metrics_interval=10,
        scheduler=custom_scheduler,
        scheduler_executor="hamster_executor",
    )

    # Create Unleash client and check initial load
    unleash_client.initialize_client()
    time.sleep(1)
    assert unleash_client.is_initialized
    assert len(unleash_client.features) >= 4

    # Simulate caching
    responses.add(
        responses.GET,
        URL + FEATURES_URL,
        json={},
        status=304,
        headers={"etag": ETAG_VALUE},
    )
    time.sleep(6)

    # Simulate server provisioning change
    responses.add(
        responses.GET,
        URL + FEATURES_URL,
        json=MOCK_ALL_FEATURES,
        status=200,
        headers={"etag": "W/somethingelse"},
    )
    time.sleep(6)
    assert len(unleash_client.features) >= 9


def test_multiple_instances_blocks_client_instantiation():
    with pytest.raises(Exception):
        UnleashClient(URL, APP_NAME, multiple_instance_mode=InstanceAllowType.BLOCK)
        UnleashClient(URL, APP_NAME, multiple_instance_mode=InstanceAllowType.BLOCK)


def test_multiple_instances_with_allow_multiple_warns(caplog):
    UnleashClient(URL, APP_NAME, multiple_instance_mode=InstanceAllowType.WARN)
    UnleashClient(URL, APP_NAME, multiple_instance_mode=InstanceAllowType.WARN)
    assert any(["You already have 1 instance" in r.msg for r in caplog.records])


def test_multiple_instances_tracks_current_instance_count(caplog):
    UnleashClient(URL, APP_NAME)
    UnleashClient(URL, APP_NAME, multiple_instance_mode=InstanceAllowType.WARN)
    UnleashClient(URL, APP_NAME, multiple_instance_mode=InstanceAllowType.WARN)
    assert any(["You already have 1 instance" in r.msg for r in caplog.records])
    assert any(["You already have 2 instance(s)" in r.msg for r in caplog.records])


def test_multiple_instances_no_warnings_or_errors_with_different_client_configs(caplog):
    UnleashClient(URL, "some-probably-unique-app-name")
    UnleashClient(
        URL,
        "some-probably-unique-app-name",
        instance_id="some-unique-instance-id",
        refresh_interval="60",
    )
    UnleashClient(
        URL, "some-probably-unique-but-different-app-name", refresh_interval="60"
    )
    assert not any(
        ["Multiple instances has been disabled" in r.msg for r in caplog.records]
    )


def test_multiple_instances_are_unique_on_api_key(caplog):
    UnleashClient(
        URL,
        "some-probably-unique-app-name",
        custom_headers={"Authorization": "penguins"},
    )
    UnleashClient(
        URL,
        "some-probably-unique-app-name",
        custom_headers={"Authorization": "hamsters"},
    )
    assert not any(
        ["Multiple instances has been disabled" in r.msg for r in caplog.records]
    )


@responses.activate
def test_signals_feature_flag(cache):
    # Set up API
    responses.add(responses.POST, URL + REGISTER_URL, json={}, status=202)
    responses.add(
        responses.GET, URL + FEATURES_URL, json=MOCK_FEATURE_RESPONSE, status=200
    )
    responses.add(responses.POST, URL + METRICS_URL, json={}, status=202)

    # Set up signals
    send_data = signal("send-data")

    @send_data.connect
    def receive_data(sender, **kw):
        print("Caught signal from %r, data %r" % (sender, kw))

        if kw["data"].event_type == UnleashEventType.FEATURE_FLAG:
            assert kw["data"].feature_name == "testFlag"
            assert kw["data"].enabled
        elif kw["data"].event_type == UnleashEventType.VARIANT:
            assert kw["data"].feature_name == "testVariations"
            assert kw["data"].enabled
            assert kw["data"].variant == "VarA"

        raise Exception("Random!")

    def example_callback(event: UnleashEvent):
        send_data.send("anonymous", data=event)

    # Set up Unleash
    unleash_client = UnleashClient(
        URL,
        APP_NAME,
        refresh_interval=REFRESH_INTERVAL,
        metrics_interval=METRICS_INTERVAL,
        cache=cache,
        event_callback=example_callback,
    )

    # Create Unleash client and check initial load
    unleash_client.initialize_client()
    time.sleep(1)

    assert unleash_client.is_enabled("testFlag")
    variant = unleash_client.get_variant("testVariations", context={"userId": "2"})
    assert variant["name"] == "VarA"
