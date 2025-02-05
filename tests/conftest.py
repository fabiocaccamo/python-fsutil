import os
import tempfile

import pytest


@pytest.fixture
def temp_path():
    with tempfile.TemporaryDirectory() as temp_dir:

        def _temp_path(filepath=""):
            return os.path.join(temp_dir, filepath)

        yield _temp_path
