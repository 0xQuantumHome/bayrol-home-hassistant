"""Support for Bayrol switch entities."""

from __future__ import annotations

import json
import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    BAYROL_DEVICE_ID,
    BAYROL_DEVICE_TYPE,
    DOMAIN,
    SENSOR_TYPES_AUTOMATIC_CL_PH,
    SENSOR_TYPES_AUTOMATIC_SALT,
    SENSOR_TYPES_PM5_CHLORINE,
)
from .helpers import normalize_entity_id_part

_LOGGER = logging.getLogger(__name__)


def _switch_definitions(device_type: str) -> dict[str, dict[str, Any]]:
    """Return entity definitions for the configured device model."""
    if device_type == "Automatic SALT":
        return SENSOR_TYPES_AUTOMATIC_SALT
    if device_type == "Automatic Cl-pH":
        return SENSOR_TYPES_AUTOMATIC_CL_PH
    if device_type == "PM5 Chlorine":
        return SENSOR_TYPES_PM5_CHLORINE
    return {}


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Bayrol switch entities."""
    mqtt_manager = hass.data[DOMAIN][config_entry.entry_id]["mqtt_manager"]
    definitions = _switch_definitions(config_entry.data[BAYROL_DEVICE_TYPE])
    entities = []

    for topic, switch_config in definitions.items():
        if switch_config.get("entity_type") != "switch":
            continue

        entity = BayrolSwitch(config_entry, topic, switch_config)
        mqtt_manager.subscribe(
            topic, lambda value, switch=entity: switch.handle_mqtt_value(value)
        )
        entities.append(entity)

    async_add_entities(entities)


class BayrolSwitch(SwitchEntity):
    """Representation of a writable Bayrol on/off setting."""

    _attr_should_poll = False

    def __init__(
        self,
        config_entry: ConfigEntry,
        topic: str,
        switch_config: dict[str, Any],
    ) -> None:
        """Initialize a Bayrol switch."""
        self._config_entry = config_entry
        self._state_topic = topic
        self._on_value = str(switch_config["on_value"])
        self._off_value = str(switch_config["off_value"])
        self._attr_name = switch_config.get("name", topic)
        self._attr_icon = switch_config.get("icon")
        self._attr_unique_id = f"{config_entry.entry_id}_{topic}"
        device_id = normalize_entity_id_part(config_entry.data[BAYROL_DEVICE_ID])
        name = normalize_entity_id_part(self._attr_name)
        self.entity_id = f"switch.bayrol_{device_id}_{name}"
        self._attr_is_on = None

    def handle_mqtt_value(self, value: Any) -> None:
        """Update the switch from a Bayrol MQTT value."""
        value = str(value)
        if value == self._on_value:
            self._attr_is_on = True
        elif value == self._off_value:
            self._attr_is_on = False
        else:
            _LOGGER.warning(
                "Unexpected MQTT value %s for Bayrol switch %s",
                value,
                self._state_topic,
            )
            return

        if self.hass is not None:
            self.schedule_update_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the Bayrol setting on."""
        self._publish_value(self._on_value)

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the Bayrol setting off."""
        self._publish_value(self._off_value)

    def _publish_value(self, value: str) -> None:
        """Publish a setting to the Bayrol MQTT broker."""
        topic = (
            f"d02/{self._config_entry.data[BAYROL_DEVICE_ID]}"
            f"/s/{self._state_topic}"
        )
        # Integer codes (e.g. PM5 "7408") must be published without a decimal
        # point to match the select wire format; Automatic codes like "19.17"
        # stay floats.
        numeric_value = int(value) if value.isdigit() else float(value)
        payload = json.dumps({"t": self._state_topic, "v": numeric_value})
        mqtt_manager = self.hass.data[DOMAIN][self._config_entry.entry_id][
            "mqtt_manager"
        ]
        mqtt_manager.client.publish(topic, payload)
        _LOGGER.debug("Published MQTT message to %s: %s", topic, payload)

    @property
    def device_info(self) -> DeviceInfo:
        """Return the Bayrol device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._config_entry.data[BAYROL_DEVICE_ID])},
            manufacturer="Bayrol",
        )
