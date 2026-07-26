"""Support for Bayrol number entities."""

from __future__ import annotations

import json
import logging

from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    BAYROL_DEVICE_ID,
    BAYROL_DEVICE_TYPE,
    DOMAIN,
    NUMBER_TYPES_PM5_CHLORINE,
)
from .helpers import normalize_entity_id_part

_LOGGER = logging.getLogger(__name__)


def _handle_number_value(entity: BayrolNumber, value) -> None:
    """Handle an incoming number value."""
    try:
        entity._attr_native_value = float(value) / entity._coefficient
    except (TypeError, ValueError):
        _LOGGER.warning(
            "Invalid MQTT value %s for number: %s", value, entity._attr_name
        )
        return

    if entity.hass is not None:
        entity.schedule_update_ha_state()


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Bayrol number entities."""
    if config_entry.data[BAYROL_DEVICE_TYPE] != "PM5 Chlorine":
        async_add_entities([])
        return

    mqtt_manager = hass.data[DOMAIN][config_entry.entry_id]["mqtt_manager"]
    entities = []

    for topic, number_config in NUMBER_TYPES_PM5_CHLORINE.items():
        entity = BayrolNumber(config_entry, topic, number_config)
        mqtt_manager.subscribe(
            topic, lambda value, number=entity: _handle_number_value(number, value)
        )
        entities.append(entity)

    async_add_entities(entities)


class BayrolNumber(NumberEntity):
    """Representation of a writable Bayrol number."""

    def __init__(self, config_entry, topic, number_config) -> None:
        """Initialize the number entity."""
        self._config_entry = config_entry
        self._topic = topic
        self._coefficient = number_config["coefficient"]
        self._attr_name = number_config["name"]
        self._attr_device_class = number_config["device_class"]
        self._attr_native_unit_of_measurement = number_config["unit_of_measurement"]
        self._attr_native_min_value = number_config["min_value"]
        self._attr_native_max_value = number_config["max_value"]
        self._attr_native_step = number_config["step"]
        self._attr_native_value = None
        self._attr_unique_id = f"{config_entry.entry_id}_{topic}"

        device_id = normalize_entity_id_part(config_entry.data[BAYROL_DEVICE_ID])
        name = normalize_entity_id_part(number_config["name"])
        self.entity_id = f"number.bayrol_{device_id}_{name}"

    async def async_set_native_value(self, value: float) -> None:
        """Publish a new native value to the Bayrol MQTT topic."""
        mqtt_value = round(value * self._coefficient)
        topic = f"d02/{self._config_entry.data[BAYROL_DEVICE_ID]}/s/{self._topic}"
        payload = json.dumps(
            {"t": self._topic, "v": mqtt_value}, separators=(",", ":")
        )

        self.hass.data[DOMAIN][self._config_entry.entry_id][
            "mqtt_manager"
        ].client.publish(topic, payload)
        _LOGGER.debug("Published MQTT message: %s", payload)

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._config_entry.data[BAYROL_DEVICE_ID])},
            manufacturer="Bayrol",
        )
