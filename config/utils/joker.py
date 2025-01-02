"""
You can find the handy tool in this section.
"""


def resolve_bool(value: str | None, default):
    if value is None:
        return default
    value = value.lower().strip()
    if value == "false" or value == "true":
        return value == "true"  # True or False
    return default


def resolve_int(value: str | None, default):
    import contextlib

    if value is None:
        return default
    with contextlib.suppress(ValueError):
        return int(value)
    return default

