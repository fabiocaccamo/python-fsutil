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
    units = [item.lower() for item in SIZE_UNITS]
    parts = size.strip().replace("  ", " ").split(" ")
    amount = float(parts[0])
    unit = parts[1]
    factor = units.index(unit.lower())
    if not factor:
        return amount
    return int((1024**factor) * amount)
