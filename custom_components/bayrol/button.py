"""Support for Bayrol button entities."""

from __future__ import annotations

import logging

from homeassistant.components.button import ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.device_registry import DeviceInfo

from .const import (
    DOMAIN,
    SENSOR_TYPES_AUTOMATIC_SALT,
    SENSOR_TYPES_AUTOMATIC_CL_PH,
    SENSOR_TYPES_PM5_CHLORINE,
    BAYROL_DEVICE_ID,
    BAYROL_DEVICE_TYPE,
)
from .helpers import normalize_entity_id_part

_LOGGER = logging.getLogger(__name__)


def _sensor_types_for_device(device_type: str) -> dict:
    """Return the sensor type dict matching the configured device type."""
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
    """Set up the Bayrol button entities."""
    entities: list[BayrolButton] = []
    device_type = config_entry.data[BAYROL_DEVICE_TYPE]
    sensor_types = _sensor_types_for_device(device_type)

    for topic, config in sensor_types.items():
        if config.get("entity_type") != "button":
            continue
        for action_name, mqtt_value in config.get("actions", {}).items():
            entities.append(
                BayrolButton(config_entry, topic, config, action_name, mqtt_value)
            )

    async_add_entities(entities)


class BayrolButton(ButtonEntity):
    """Representation of a Bayrol button entity."""

    def __init__(self, config_entry, topic, config, action_name, mqtt_value):
        """Initialize the button entity."""
        self._config_entry = config_entry
        self._topic = topic
        self._mqtt_value = mqtt_value
        base_name = config.get("name", topic)
        self._attr_name = f"{base_name} {action_name}"
        self._attr_unique_id = f"{config_entry.entry_id}_{topic}_{action_name}"
        device_id = normalize_entity_id_part(config_entry.data[BAYROL_DEVICE_ID])
        object_id = normalize_entity_id_part(f"{base_name} {action_name}")
        self.entity_id = f"button.bayrol_{device_id}_{object_id}"

    async def async_press(self) -> None:
        """Publish the configured MQTT value for this button."""
        topic = f"d02/{self._config_entry.data[BAYROL_DEVICE_ID]}/s/{self._topic}"
        payload = f'{{"t":"{self._topic}","v":{self._mqtt_value}}}'
        self.hass.data[DOMAIN][self._config_entry.entry_id][
            "mqtt_manager"
        ].client.publish(topic, payload)
        _LOGGER.debug("Published MQTT message: %s", payload)

    @property
    def device_info(self) -> DeviceInfo:
        """Device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._config_entry.data[BAYROL_DEVICE_ID])},
            manufacturer="Bayrol",
        )
