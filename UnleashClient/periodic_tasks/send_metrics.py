from collections import ChainMap
from datetime import datetime
from UnleashClient.api import send_metrics


def aggregate_and_send_metrics(url: str,
                               app_name: str,
                               instance_id: str,
                               custom_headers: dict,
                               features: dict,
                               last_sent: datetime
                               ) -> None:
    feature_stats_list = []

    for feature_name in features.keys():
        feature_stats = {
            features[feature_name].name: {
                "yes": features[feature_name].yes_count,
                "no": features[feature_name].no_count
            }
        }

        features[feature_name].reset_stats()
        feature_stats_list.append(feature_stats)

    metrics_request = {
        "appName": app_name,
        "instanceId": instance_id,
        "bucket": {
            "start": last_sent.isoformat(),
            "stop": datetime.now().isoformat(),
            "toggles": dict(ChainMap(*feature_stats_list))
        }
    }

    send_metrics(url, metrics_request, custom_headers)
    last_sent = datetime.now()
