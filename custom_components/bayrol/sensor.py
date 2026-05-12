"""Support for Bayrol sensors."""

from __future__ import annotations

import logging

from homeassistant.components.sensor import (
    SensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.device_registry import DeviceInfo

from .const import (
    DOMAIN,
    SENSOR_TYPES_AUTOMATIC_SALT,
    SENSOR_TYPES_AUTOMATIC_CL_PH,
    SENSOR_TYPES_PM5_CHLORINE,
    ALARM_TOPICS,
    BAYROL_DEVICE_ID,
    BAYROL_DEVICE_TYPE,
)
from .helpers import normalize_entity_id_part

_LOGGER = logging.getLogger(__name__)


def _handle_sensor_value(sensor, value):
    """Handle incoming sensor value."""
    # Check if this is a numeric sensor that should not be converted to strings
    is_numeric_sensor = (
        sensor._sensor_config.get("state_class") is not None
        and sensor._sensor_config.get("state_class") != "None"
        and sensor._sensor_config.get("unit_of_measurement") is not None
    )

    # If it's a numeric sensor, handle it directly without string conversion
    if is_numeric_sensor:
        if (
            sensor._sensor_config.get("coefficient") is not None
            and sensor._sensor_config["coefficient"] != -1
        ):
            sensor._attr_native_value = value / sensor._sensor_config["coefficient"]
        else:
            sensor._attr_native_value = value
    else:
        # Handle string conversion for non-numeric sensors
        match value:
            case "19.18":
                sensor._attr_native_value = "On"
            case "19.19":
                sensor._attr_native_value = "Off"
            case "19.95":
                sensor._attr_native_value = "Filtration is off"
            case "19.96":
                sensor._attr_native_value = "Filtration is on"
            case "19.105":
                sensor._attr_native_value = "Water detected"
            case "19.147":
                sensor._attr_native_value = "Stopped (gas detected)"
            case "19.195":
                sensor._attr_native_value = "Auto"
            case "19.115":
                sensor._attr_native_value = "Auto Plus"
            case "19.106":
                sensor._attr_native_value = "Constant production"
            case "19.177":
                sensor._attr_native_value = "On"
            case "19.176":
                sensor._attr_native_value = "Off"
            case "19.257":
                sensor._attr_native_value = "Missing"
            case "19.258":
                sensor._attr_native_value = "Not Empty"
            case "19.259":
                sensor._attr_native_value = "Empty"
            case "19.311":
                sensor._attr_native_value = "ON"
            case "19.312":
                sensor._attr_native_value = "OFF"
            case "19.315":
                sensor._attr_native_value = "Low"
            case "19.316":
                sensor._attr_native_value = "Med"
            case "19.317":
                sensor._attr_native_value = "High"
            case "19.346":
                sensor._attr_native_value = "Auto"
            case 7001:
                sensor._attr_native_value = "On"
            case 7002:
                sensor._attr_native_value = "Off"
            case 7521:
                sensor._attr_native_value = "Full"
            case 7522:
                sensor._attr_native_value = "Low"
            case 7523:
                sensor._attr_native_value = "Empty"
            case 7524:
                sensor._attr_native_value = "Ok"
            case 7525:
                sensor._attr_native_value = "Info"
            case 7526:
                sensor._attr_native_value = "Warning"
            case 7527:
                sensor._attr_native_value = "Alarm"
            case _:
                if (
                    sensor._sensor_config.get("coefficient") is not None
                    and sensor._sensor_config["coefficient"] != -1
                ):
                    sensor._attr_native_value = (
                        value / sensor._sensor_config["coefficient"]
                    )
                elif sensor._sensor_config.get("coefficient") == -1:
                    sensor._attr_native_value = str(value)
                else:
                    sensor._attr_native_value = value

    if sensor.hass is not None:
        sensor.schedule_update_ha_state()


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Bayrol sensor."""
    entities = []
    device_type = config_entry.data[BAYROL_DEVICE_TYPE]
    _LOGGER.debug("device_type: %s", device_type)

    # Get the MQTT manager for this specific config entry
    mqtt_manager = hass.data[DOMAIN][config_entry.entry_id]["mqtt_manager"]

    type_map = {
        "Automatic SALT": SENSOR_TYPES_AUTOMATIC_SALT,
        "Automatic Cl-pH": SENSOR_TYPES_AUTOMATIC_CL_PH,
        "PM5 Chlorine": SENSOR_TYPES_PM5_CHLORINE,
    }
    sensor_types = type_map.get(device_type, {})

    for sensor_type, sensor_config in sensor_types.items():
        # Skip select entities (handled by select platform)
        if sensor_config.get("entity_type") == "select":
            continue
        # Skip alarm topics (handled by binary_sensor platform)
        if sensor_type in ALARM_TOPICS:
            continue
        sensor = BayrolSensor(config_entry, sensor_type, sensor_config, sensor_type)
        mqtt_manager.subscribe(
            sensor_type, lambda v, s=sensor: _handle_sensor_value(s, v)
        )
        entities.append(sensor)

    async_add_entities(entities)


class BayrolSensor(SensorEntity):
    """Representation of a Bayrol sensor."""

    def __init__(self, config_entry, sensor_type, sensor_config, topic):
        """Initialize the sensor."""
        self._config_entry = config_entry
        self._sensor_type = sensor_type
        self._sensor_config = sensor_config
        self._state_topic = topic
        self._attr_name = sensor_config.get("name", sensor_type)
        self._attr_device_class = sensor_config.get("device_class")
        self._attr_state_class = sensor_config.get("state_class")
        self._attr_native_unit_of_measurement = sensor_config.get("unit_of_measurement")
        self._attr_unique_id = f"{config_entry.entry_id}_{sensor_type}"
        device_id = normalize_entity_id_part(config_entry.data[BAYROL_DEVICE_ID])
        name = normalize_entity_id_part(sensor_config.get("name", sensor_type))
        self.entity_id = f"sensor.bayrol_{device_id}_{name}"
        coefficient = sensor_config.get("coefficient")
        if coefficient == 1:
            self._attr_suggested_display_precision = 0
        elif coefficient == 10:
            self._attr_suggested_display_precision = 1
        elif coefficient == 100:
            self._attr_display_precision = 2
        self._attr_native_value = None

    async def async_added_to_hass(self) -> None:
        """Run when entity is added to Home Assistant."""
        pass

    @property
    def device_info(self) -> DeviceInfo:
        """Device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._config_entry.data[BAYROL_DEVICE_ID])},
            manufacturer="Bayrol",
        )
