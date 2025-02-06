from types import ModuleType


def require_requests() -> ModuleType:
    try:
        import requests

        return requests
    except ImportError as error:
        raise ModuleNotFoundError(
            "'requests' module is not installed, "
            "it can be installed by running: 'pip install requests'"
        ) from error
