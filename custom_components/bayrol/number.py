"""Support for Bayrol number entities."""

from __future__ import annotations

import logging
import math

import paho.mqtt.client as mqtt

from homeassistant.components.number import NumberEntity, NumberMode
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
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


def _value_matches_step(value: float, minimum: float, step: float) -> bool:
    """Return whether value is aligned to step from the minimum value."""
    if step <= 0:
        return True
    increments = (value - minimum) / step
    return math.isclose(increments, round(increments), rel_tol=0.0, abs_tol=1e-6)


def _sensor_types_for_device(device_type: str) -> dict:
    """Return the sensor type dict matching the configured device type."""
    if device_type == "Automatic SALT":
        return SENSOR_TYPES_AUTOMATIC_SALT
    if device_type == "Automatic Cl-pH":
        return SENSOR_TYPES_AUTOMATIC_CL_PH
    if device_type == "PM5 Chlorine":
        return SENSOR_TYPES_PM5_CHLORINE
    return {}


def _handle_number_value(number, value):
    """Handle an incoming MQTT value for a number entity."""
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        _LOGGER.warning(
            "Unexpected payload %r for %s", value, number._attr_name
        )
        return
    try:
        coefficient = number._number_config.get("coefficient")
        if coefficient is not None and coefficient != -1:
            number._attr_native_value = float(value) / coefficient
        else:
            number._attr_native_value = float(value)
    except (ValueError, TypeError) as e:
        _LOGGER.warning(
            "Invalid numeric value %s for %s: %s", value, number._attr_name, e
        )
        return

    if number.hass is not None:
        number.schedule_update_ha_state()


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Bayrol number entities."""
    entities = []
    device_type = config_entry.data[BAYROL_DEVICE_TYPE]
    mqtt_manager = hass.data[DOMAIN][config_entry.entry_id]["mqtt_manager"]

    for number_type, number_config in _sensor_types_for_device(device_type).items():
        if number_config.get("entity_type") != "number":
            continue
        topic = number_type
        number = BayrolNumber(config_entry, number_type, number_config, topic)
        mqtt_manager.subscribe(topic, lambda v, n=number: _handle_number_value(n, v))
        entities.append(number)

    async_add_entities(entities)


class BayrolNumber(NumberEntity):
    """Representation of a Bayrol number entity."""

    def __init__(self, config_entry, number_type, number_config, topic):
        """Initialize the number entity."""
        self._config_entry = config_entry
        self._number_type = number_type
        self._number_config = number_config
        self._state_topic = topic
        self._attr_name = number_config.get("name", number_type)
        self._attr_unique_id = f"{config_entry.entry_id}_{number_type}"
        device_id = normalize_entity_id_part(config_entry.data[BAYROL_DEVICE_ID])
        name = normalize_entity_id_part(number_config.get("name", number_type))
        self.entity_id = f"number.bayrol_{device_id}_{name}"
        self._attr_device_class = number_config.get("device_class")
        self._attr_native_unit_of_measurement = number_config.get(
            "unit_of_measurement"
        )
        self._attr_native_min_value = number_config.get("min", 0.0)
        self._attr_native_max_value = number_config.get("max", 100.0)
        self._attr_native_step = number_config.get("step", 1.0)
        self._attr_mode = number_config.get("mode", NumberMode.BOX)
        self._attr_entity_registry_enabled_default = number_config.get(
            "enabled_default", True
        )
        self._attr_native_value = None

    async def async_set_native_value(self, value: float) -> None:
        """Encode the value, publish it and update the state optimistically."""
        native_value = float(value)
        minimum = float(self._attr_native_min_value)
        maximum = float(self._attr_native_max_value)
        step = float(self._attr_native_step)
        if native_value < minimum or native_value > maximum:
            raise HomeAssistantError(
                f"Value {native_value} for {self._attr_name} must be between "
                f"{minimum} and {maximum}"
            )
        if not _value_matches_step(native_value, minimum, step):
            raise HomeAssistantError(
                f"Value {native_value} for {self._attr_name} must use step {step} "
                f"from {minimum}"
            )

        coefficient = self._number_config.get("coefficient")
        if coefficient is not None and coefficient != -1:
            mqtt_value = str(int(native_value * coefficient + 0.5))
        else:
            mqtt_value = str(int(native_value + 0.5))

        client = self.hass.data[DOMAIN][self._config_entry.entry_id][
            "mqtt_manager"
        ].client
        if client is None or not client.is_connected():
            raise HomeAssistantError("Bayrol MQTT connection not available")

        topic = f"d02/{self._config_entry.data[BAYROL_DEVICE_ID]}/s/{self._state_topic}"
        payload = f'{{"t":"{self._state_topic}","v":{mqtt_value}}}'
        result = client.publish(topic, payload)
        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            raise HomeAssistantError(
                f"Failed to publish Bayrol setpoint (rc={result.rc})"
            )
        _LOGGER.debug("Published MQTT message: %s", payload)

        # Optimistic update; the device echo on the v/ topic confirms/corrects it.
        self._attr_native_value = native_value
        self.async_write_ha_state()

    @property
    def device_info(self) -> DeviceInfo:
        """Device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._config_entry.data[BAYROL_DEVICE_ID])},
            manufacturer="Bayrol",
        )
