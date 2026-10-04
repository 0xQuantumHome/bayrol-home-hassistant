"""Helper functions for the Bayrol integration."""

import re

# Automatic enum values ("19.<id>") must be sent as JSON strings, exactly like
# the official web app does (DeviceDriver.js getPublishJson). As bare JSON
# numbers, trailing zeros are lost: 19.100 (Out Off) arrives as 19.1.
_AUTOMATIC_ENUM_VALUE = re.compile(r"^19\.\d+$")


def build_set_payload(topic: str, value) -> str:
    """Build the compact JSON payload for a Bayrol set command.

    The device firmware ignores payloads containing whitespace, so the JSON
    is assembled by hand instead of with json.dumps defaults (see #51).
    """
    value_str = str(value)
    if _AUTOMATIC_ENUM_VALUE.match(value_str):
        value_str = f'"{value_str}"'
    return f'{{"t":"{topic}","v":{value_str}}}'


def normalize_entity_id_part(value: str) -> str:
    """Normalize a string for use in a Home Assistant entity_id object_id.

    Only lowercase letters, digits and underscores are allowed.
    """
    s = value.lower().replace(" ", "_")
    s = re.sub(r"[^a-z0-9_]", "_", s)
    return re.sub(r"_+", "_", s).strip("_") or "unknown"
