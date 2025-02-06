import pytest

import fsutil


@pytest.mark.parametrize(
    "size_bytes, expected_output",
    [
        (1023, "1023 bytes"),
        (1024, "1 KB"),
        (1048576, "1.00 MB"),
        (1572864, "1.50 MB"),
        (1073741824, "1.00 GB"),
        (1879048192, "1.75 GB"),
        (1099511627776, "1.00 TB"),
    ],
)
def test_convert_size_bytes_to_string(size_bytes, expected_output):
    assert fsutil.convert_size_bytes_to_string(size_bytes) == expected_output


@pytest.mark.parametrize(
    "size_string, expected_output",
    [
        ("1023 bytes", "1023 bytes"),
        ("1 KB", "1 KB"),
        ("1.00 MB", "1.00 MB"),
        ("1.25 MB", "1.25 MB"),
        ("2.50 MB", "2.50 MB"),
        ("1.00 GB", "1.00 GB"),
        ("1.09 GB", "1.09 GB"),
        ("1.99 GB", "1.99 GB"),
        ("1.00 TB", "1.00 TB"),
    ],
)
def test_convert_size_bytes_to_string_and_convert_size_string_to_bytes(
    size_string, expected_output
):
    assert (
        fsutil.convert_size_bytes_to_string(
            fsutil.convert_size_string_to_bytes(size_string)
        )
        == expected_output
    )


@pytest.mark.parametrize(
    "size_string, expected_output",
    [
        ("1 KB", 1024),
        ("1.00 MB", 1048576),
        ("1.00 GB", 1073741824),
        ("1.00 TB", 1099511627776),
    ],
)
def test_convert_size_string_to_bytes(size_string, expected_output):
    assert fsutil.convert_size_string_to_bytes(size_string) == expected_output


@pytest.mark.parametrize(
    "size_bytes, expected_output",
    [
        (1023, 1023),
        (1024, 1024),
        (1048576, 1048576),
        (1310720, 1310720),
        (2621440, 2621440),
        (1073741824, 1073741824),
        (1170378588, 1170378588),
        (2136746229, 2136746229),
        (1099511627776, 1099511627776),
    ],
)
def test_convert_size_string_to_bytes_and_convert_size_bytes_to_string(
    size_bytes, expected_output
):
    assert (
        fsutil.convert_size_string_to_bytes(
            fsutil.convert_size_bytes_to_string(size_bytes)
        )
        == expected_output
    )


if __name__ == "__main__":
    pytest.main()
