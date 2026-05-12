"""Binary sensors for Bayrol device alarms."""

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
    DOMAIN,
    ALARM_TOPICS,
    BAYROL_DEVICE_ID,
)
from .helpers import normalize_entity_id_part

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Bayrol binary sensors (device alarms)."""
    mqtt_manager = hass.data[DOMAIN][config_entry.entry_id]["mqtt_manager"]

    entities = []
    for topic, alarm_config in ALARM_TOPICS.items():
        sensor = BayrolAlarmBinarySensor(config_entry, topic, alarm_config)
        mqtt_manager.subscribe(
            topic, lambda payload, s=sensor: s.handle_alarm_payload(payload)
        )
        entities.append(sensor)

    async_add_entities(entities)


class BayrolAlarmBinarySensor(BinarySensorEntity):
    """
    Binary sensor representing a Bayrol device alarm.

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
        """Initialise the alarm binary sensor."""
        self._config_entry = config_entry
        self._topic = topic
        self._alarm_config = alarm_config

        device_id = normalize_entity_id_part(config_entry.data[BAYROL_DEVICE_ID])
        slug = topic.replace(".", "_")

        self._attr_name = alarm_config["name"]
        self._attr_unique_id = f"{config_entry.entry_id}_{topic}"
        self.entity_id = f"binary_sensor.bayrol_{device_id}_{slug}"

        self._attr_is_on = False
        self._quit_required: bool = False
        self._module: str | None = None
        self._is_quit: bool = False

    def handle_alarm_payload(self, payload: Any) -> None:
        """Process an incoming alarm payload dict from the MQTT manager."""
        if not isinstance(payload, dict):
            _LOGGER.warning(
                "Unexpected alarm payload type for %s: %s", self._topic, type(payload)
            )
            return

        active = payload.get("active", False)
        self._attr_is_on = bool(active)
        self._quit_required = bool(payload.get("quit_required", False))
        self._is_quit = bool(payload.get("is_quit", False))
        self._module = payload.get("module")

        _LOGGER.debug(
            "Alarm %s: active=%s quit_required=%s is_quit=%s module=%s",
            self._topic,
            active,
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
            "topic": self._topic,
            "module": self._module,
            "quit_required": self._quit_required,
            "is_quit": self._is_quit,
        }

    @property
    def device_info(self) -> DeviceInfo:
        """Link this sensor to the Bayrol device."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._config_entry.data[BAYROL_DEVICE_ID])},
            manufacturer="Bayrol",
        )
