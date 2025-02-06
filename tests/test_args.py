import os
from pathlib import Path

import pytest

from fsutil.args import get_path


@pytest.mark.parametrize(
    "input_path, expected",
    [
        (None, None),
        ("", "."),
        ("/home/user/docs", os.path.normpath("/home/user/docs")),
        ("C:\\Users\\test", os.path.normpath("C:\\Users\\test")),
        ("./relative/path", os.path.normpath("./relative/path")),
        ("..", os.path.normpath("..")),
        (Path("/home/user/docs"), os.path.normpath("/home/user/docs")),
        (Path("C:\\Users\\test"), os.path.normpath("C:\\Users\\test")),
        (Path("./relative/path"), os.path.normpath("./relative/path")),
        (Path(".."), os.path.normpath("..")),
    ],
)
def test_get_path(input_path, expected):
    assert get_path(input_path) == expected


if __name__ == "__main__":
    pytest.main()
