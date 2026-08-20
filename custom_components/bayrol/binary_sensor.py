"""Binary sensors for Bayrol device states and alarms.

Alarm protocol discovered by @davifernan (PR #33): the device publishes
dict payloads without a "v" key on topics 8.2002/8.2003.
"""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    ALARM_TOPICS,
    BAYROL_DEVICE_ID,
    BAYROL_DEVICE_TYPE,
    DOMAIN,
    SENSOR_TYPES_AUTOMATIC_CL_PH,
    SENSOR_TYPES_AUTOMATIC_SALT,
    SENSOR_TYPES_PM5_CHLORINE,
)
from .helpers import normalize_entity_id_part

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Bayrol binary sensors."""
    mqtt_manager = hass.data[DOMAIN][config_entry.entry_id]["mqtt_manager"]

    entities = []

    device_type = config_entry.data[BAYROL_DEVICE_TYPE]
    sensor_types = {
        "Automatic SALT": SENSOR_TYPES_AUTOMATIC_SALT,
        "Automatic Cl-pH": SENSOR_TYPES_AUTOMATIC_CL_PH,
        "PM5 Chlorine": SENSOR_TYPES_PM5_CHLORINE,
    }.get(device_type, {})

    for topic, sensor_config in sensor_types.items():
        if sensor_config.get("entity_type") != "binary_sensor":
            continue

        sensor = BayrolStateBinarySensor(config_entry, topic, sensor_config)
        mqtt_manager.subscribe(
            topic, lambda payload, s=sensor: s.handle_state_payload(payload)
        )
        entities.append(sensor)

    # The 8.2002/8.2003 alarm topics only exist on PM5 devices; Automatic
    # devices report their message state on topic 10 instead (verified via
    # a full topic capture in #51).
    if device_type == "PM5 Chlorine":
        for topic, alarm_config in ALARM_TOPICS.items():
            sensor = BayrolAlarmBinarySensor(config_entry, topic, alarm_config)
            mqtt_manager.subscribe(
                topic, lambda payload, s=sensor: s.handle_alarm_payload(payload)
            )
            entities.append(sensor)

    async_add_entities(entities)


class BayrolStateBinarySensor(BinarySensorEntity):
    """Binary sensor representing a two-state Bayrol MQTT value."""

    _attr_should_poll = False

    def __init__(
        self,
        config_entry: ConfigEntry,
        topic: str,
        sensor_config: dict[str, Any],
    ) -> None:
        """Initialize the state binary sensor."""
        self._config_entry = config_entry
        self._state_topic = topic
        self._sensor_config = sensor_config
        self._attr_name = sensor_config.get("name", topic)
        self._attr_device_class = sensor_config.get("device_class")
        self._attr_unique_id = f"{config_entry.entry_id}_{topic}"
        device_id = normalize_entity_id_part(config_entry.data[BAYROL_DEVICE_ID])
        name = normalize_entity_id_part(sensor_config.get("name", topic))
        self.entity_id = f"binary_sensor.bayrol_{device_id}_{name}"
        self._attr_is_on = None
        self._raw_value: Any = None

    def handle_state_payload(self, payload: Any) -> None:
        """Process a two-state MQTT payload without guessing unknown values."""
        # Broker payloads are untrusted; cap what we keep and log.
        value = str(payload)[:64]
        previous_raw = self._raw_value
        self._raw_value = value

        if value in self._sensor_config.get("on_values", ()):
            self._attr_is_on = True
        elif value in self._sensor_config.get("off_values", ()):
            self._attr_is_on = False
        else:
            # Keep the last known state instead of dropping to unknown on a
            # single malformed message; warn once per distinct value.
            if value != previous_raw:
                _LOGGER.warning(
                    "Unexpected value %r for binary sensor %s (topic %s)",
                    value,
                    self._attr_name,
                    self._state_topic,
                )

        if self.hass is not None:
            self.schedule_update_ha_state()

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the raw Bayrol value for diagnostics."""
        return {"raw_value": self._raw_value, "topic": self._state_topic}

    @property
    def device_info(self) -> DeviceInfo:
        """Device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._config_entry.data[BAYROL_DEVICE_ID])},
            manufacturer="Bayrol",
        )


class BayrolAlarmBinarySensor(BinarySensorEntity):
    """Binary sensor representing a Bayrol device alarm.

    on  = alarm is active
    off = no active alarm
    """

    _attr_device_class = BinarySensorDeviceClass.PROBLEM
    _attr_should_poll = False

    def __init__(
        self,
        config_entry: ConfigEntry,
        topic: str,
        alarm_config: dict[str, Any],
    ) -> None:
        """Initialize the alarm binary sensor."""
        self._config_entry = config_entry
        self._state_topic = topic
        self._alarm_config = alarm_config
        self._attr_name = alarm_config.get("name", topic)
        self._attr_unique_id = f"{config_entry.entry_id}_{topic}"
        device_id = normalize_entity_id_part(config_entry.data[BAYROL_DEVICE_ID])
        name = normalize_entity_id_part(alarm_config.get("name", topic))
        self.entity_id = f"binary_sensor.bayrol_{device_id}_{name}"
        self._attr_is_on = False
        self._quit_required: bool = False
        self._module: str | None = None
        self._is_quit: bool = False

    def handle_alarm_payload(self, payload: Any) -> None:
        """Process an incoming alarm payload dict from the MQTT manager."""
        if not isinstance(payload, dict):
            _LOGGER.warning(
                "Unexpected alarm payload type for %s: %s",
                self._state_topic,
                type(payload),
            )
            return

        self._attr_is_on = bool(payload.get("active", False))
        self._quit_required = bool(payload.get("quit_required", False))
        self._is_quit = bool(payload.get("is_quit", False))
        self._module = payload.get("module")

        _LOGGER.debug(
            "Alarm %s: active=%s quit_required=%s is_quit=%s module=%s",
            self._state_topic,
            self._attr_is_on,
            self._quit_required,
            self._is_quit,
            self._module,
        )

        if self.hass is not None:
            self.schedule_update_ha_state()

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional alarm metadata as HA attributes."""
        return {
            "topic": self._state_topic,
            "module": self._module,
            "quit_required": self._quit_required,
            "is_quit": self._is_quit,
        }

    @property
    def device_info(self) -> DeviceInfo:
        """Device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._config_entry.data[BAYROL_DEVICE_ID])},
            manufacturer="Bayrol",
        )
