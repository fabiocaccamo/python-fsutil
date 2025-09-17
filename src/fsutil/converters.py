from __future__ import annotations

SIZE_UNITS = ["bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]


def convert_size_bytes_to_string(size: int) -> str:
    """
    Convert the given size bytes to string using the right unit suffix.
    """
    size_num = float(size)
    units = SIZE_UNITS
    factor = 0
    factor_limit = len(units) - 1
    while (size_num >= 1024) and (factor <= factor_limit):
        size_num /= 1024
        factor += 1
    size_units = units[factor]
    size_str = f"{size_num:.2f}" if (factor > 1) else f"{size_num:.0f}"
    size_str = f"{size_str} {size_units}"
    return size_str


def convert_size_string_to_bytes(size: str) -> float | int:
    """
    Convert the given size string to bytes.
    """
    if not isinstance(size, str):
        raise TypeError(f"Expected string, got {type(size).__name__}")

    units = [item.lower() for item in SIZE_UNITS]
    parts = size.strip().replace("  ", " ").split(" ")

    if len(parts) < 1:
        expected_format = "Expected format: '<number> <unit>' or '<number>'"
        raise ValueError(f"Invalid size format: '{size}'. {expected_format}")

    try:
        amount = float(parts[0])
    except ValueError as e:
        raise ValueError(f"Invalid number in size string: '{parts[0]}'") from e

    if len(parts) == 1:
        # Assume bytes if no unit specified
        return int(amount)

    if len(parts) != 2:
        expected_format = "Expected format: '<number> <unit>' or '<number>'"
        raise ValueError(f"Invalid size format: '{size}'. {expected_format}")

    unit = parts[1].lower()
    try:
        factor = units.index(unit)
    except ValueError as e:
        valid_units = ", ".join(SIZE_UNITS)
        error_msg = f"Unknown size unit: '{parts[1]}'. Valid units: {valid_units}"
        raise ValueError(error_msg) from e

    if not factor:
        return int(amount)
    return int((1024**factor) * amount)
