import sys
from types import ModuleType
from unittest import mock

import pytest

from fsutil.deps import require_requests


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


if __name__ == "__main__":
    pytest.main()
