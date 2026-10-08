import sys
from types import ModuleType
from unittest import mock

import pytest

from fsutil.deps import require_requests, require_yaml


def test_require_requests_installed():
    with mock.patch.dict(sys.modules, {"requests": mock.Mock(spec=ModuleType)}):
        requests_module = require_requests()
        assert isinstance(requests_module, ModuleType)


def test_require_requests_not_installed():
    with mock.patch.dict(sys.modules, {"requests": None}):
        with pytest.raises(
            ModuleNotFoundError, match="'requests' module is not installed"
        ):
            require_requests()


def test_require_yaml_installed():
    with mock.patch.dict(sys.modules, {"yaml": mock.Mock(spec=ModuleType)}):
        yaml_module = require_yaml()
        assert isinstance(yaml_module, ModuleType)


def test_require_yaml_not_installed():
    with mock.patch.dict(sys.modules, {"yaml": None}):
        with pytest.raises(
            ModuleNotFoundError, match="'PyYAML' module is not installed"
        ):
            require_yaml()


if __name__ == "__main__":
    pytest.main()
