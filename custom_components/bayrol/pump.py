"""Filtration pump setup detection for Automatic devices with Smart&Easy.

Topics, options and texts live in the "filtration" entry of the datapoint
table (const.py); this module only decides which of them applies.
"""

from __future__ import annotations

from collections.abc import Callable

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN


def _is_set(value) -> bool:
    """Return True for an active condition (payload 1)."""
    try:
        return int(float(value)) == 1
    except (TypeError, ValueError):
        return False


def filtration_config(sensor_types: dict) -> dict | None:
    """Return the filtration entry of a datapoint table, if it has one."""
    for config in sensor_types.values():
        if config.get("filtration"):
            return config
    return None


class BayrolPumpSetup:
    """Track the pump configuration reported by one device."""

    def __init__(self, mqtt_manager, config: dict) -> None:
        self._mode_topics = config["mode_topics"]
        self._listeners: list[Callable[[], None]] = []
        self.vsp_used: bool | None = None
        self.temp_used: bool | None = None
        self._out_assigned: dict[int, bool] = {}

        conditions = config["conditions"]
        mqtt_manager.subscribe(conditions["vsp_used"], self._on_vsp_used)
        mqtt_manager.subscribe(conditions["temp_used"], self._on_temp_used)
        mqtt_manager.subscribe(conditions["temp_not_used"], self._on_temp_not_used)
        for topic, out in conditions["out_filter_pump"].items():
            mqtt_manager.subscribe(
                topic, lambda v, out=out: self._on_out_assigned(out, v)
            )

    def add_listener(self, listener: Callable[[], None]) -> None:
        """Call listener whenever the detected setup changes."""
        self._listeners.append(listener)

    def _changed(self) -> None:
        for listener in list(self._listeners):
            listener()

    def _on_vsp_used(self, value) -> None:
        self.vsp_used = _is_set(value)
        self._changed()

    def _on_temp_used(self, value) -> None:
        if _is_set(value):
            self.temp_used = True
            self._changed()

    def _on_temp_not_used(self, value) -> None:
        if _is_set(value):
            self.temp_used = False
            self._changed()

    def _on_out_assigned(self, out: int, value) -> None:
        self._out_assigned[out] = _is_set(value)
        self._changed()

    @property
    def pump_out(self) -> int | None:
        """OUT number a fixed speed filter pump is wired to, if any."""
        for out, assigned in sorted(self._out_assigned.items()):
            if assigned:
                return out
        return None

    @property
    def mode_topic(self) -> str | None:
        """Active filtration mode datapoint, None if not (yet) known."""
        if self.temp_used is None:
            return None
        temp = "temp" if self.temp_used else "no_temp"
        if self.vsp_used:
            return self._mode_topics[f"vsp_{temp}"]
        if self.pump_out is not None:
            return self._mode_topics[f"fixed_{temp}"]
        return None


def get_pump_setup(
    hass: HomeAssistant, entry: ConfigEntry, sensor_types: dict
) -> BayrolPumpSetup:
    """Return the shared pump setup tracker of a config entry."""
    entry_data = hass.data[DOMAIN][entry.entry_id]
    if "pump_setup" not in entry_data:
        entry_data["pump_setup"] = BayrolPumpSetup(
            entry_data["mqtt_manager"], filtration_config(sensor_types)
        )
    return entry_data["pump_setup"]
