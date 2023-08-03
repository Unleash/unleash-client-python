import warnings

from UnleashClient.strategies import Strategy


def strategy_v2xx_deprecation_check(strategies: list) -> None:
    """
    Notify users of backwards incompatible changes in v3 for custom strategies.
    """
    for strategy in strategies:
        try:
            # Check if the __call__() method is overwritten (should only be true for custom strategies in v1.x or v2.x.
            if strategy.__call__ != Strategy.__call__:  # type:ignore
                warnings.warn(
                    f"unleash-client-python v3.x.x requires overriding the execute() method instead of the __call__() method. Error in: {strategy.__name__}",
                    DeprecationWarning,
                )
        except AttributeError:
            # Ignore if not.
            pass
