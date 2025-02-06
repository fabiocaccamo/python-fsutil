import pytest

from fsutil.metadata import (
    __author__,
    __copyright__,
    __description__,
    __email__,
    __license__,
    __title__,
    __version__,
)


def test_metadata_variables():
    assert bool(__author__) and isinstance(__author__, str)
    assert bool(__copyright__) and isinstance(__copyright__, str)
    assert bool(__description__) and isinstance(__description__, str)
    assert bool(__email__) and isinstance(__email__, str)
    assert bool(__license__) and isinstance(__license__, str)
    assert bool(__title__) and isinstance(__title__, str)
    assert bool(__version__) and isinstance(__version__, str)


if __name__ == "__main__":
    pytest.main()
