"""Helper functions for the Bayrol integration."""

import re


def normalize_entity_id_part(value: str) -> str:
    """Normalize a string for use in a Home Assistant entity_id object_id.

    Only lowercase letters, digits and underscores are allowed.
    """
    s = value.lower().replace(" ", "_")
    s = re.sub(r"[^a-z0-9_]", "_", s)
    return re.sub(r"_+", "_", s).strip("_") or "unknown"
