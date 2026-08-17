"""Read-only cover entities for Bayrol devices."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.cover import CoverEntity, CoverEntityFeature
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


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up read-only Bayrol covers."""
    mqtt_manager = hass.data[DOMAIN][config_entry.entry_id]["mqtt_manager"]
    device_type = config_entry.data[BAYROL_DEVICE_TYPE]
    sensor_types = {
        "Automatic SALT": SENSOR_TYPES_AUTOMATIC_SALT,
        "Automatic Cl-pH": SENSOR_TYPES_AUTOMATIC_CL_PH,
        "PM5 Chlorine": SENSOR_TYPES_PM5_CHLORINE,
    }.get(device_type, {})

    entities = []
    for topic, cover_config in sensor_types.items():
        if cover_config.get("entity_type") != "cover":
            continue

        cover = BayrolCover(config_entry, topic, cover_config)
        mqtt_manager.subscribe(
            topic, lambda payload, entity=cover: entity.handle_state_payload(payload)
        )
        entities.append(cover)

    async_add_entities(entities)


class BayrolCover(CoverEntity):
    """Read-only representation of a Bayrol pool cover state."""

    _attr_should_poll = False
    _attr_supported_features = CoverEntityFeature(0)

    def __init__(
        self,
        config_entry: ConfigEntry,
        topic: str,
        cover_config: dict[str, Any],
    ) -> None:
        """Initialize the cover."""
        self._config_entry = config_entry
        self._state_topic = topic
        self._cover_config = cover_config
        self._attr_name = cover_config.get("name", topic)
        self._attr_device_class = cover_config.get("device_class")
        self._attr_unique_id = f"{config_entry.entry_id}_{topic}"
        device_id = normalize_entity_id_part(config_entry.data[BAYROL_DEVICE_ID])
        name = normalize_entity_id_part(cover_config.get("name", topic))
        self.entity_id = f"cover.bayrol_{device_id}_{name}"
        self._attr_is_closed = None
        self._raw_value: Any = None

    def handle_state_payload(self, payload: Any) -> None:
        """Process a cover state without exposing unsupported controls."""
        self._raw_value = payload
        value = str(payload)

        if value in self._cover_config.get("open_values", ()):
            self._attr_is_closed = False
        elif value in self._cover_config.get("closed_values", ()):
            self._attr_is_closed = True
        elif value in self._cover_config.get("unknown_values", ()):
            self._attr_is_closed = None
        else:
            self._attr_is_closed = None
            _LOGGER.warning(
                "Unexpected value %r for cover %s (topic %s)",
                payload,
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
