"""Event entity for Bayrol PoolAccess messages.

Every newly appearing message on topic 10 is recorded as its own timestamped
event, so the logbook keeps a full chronological message history even though
the Messages sensor only shows the current snapshot.
"""

from __future__ import annotations

import logging

from homeassistant.components.event import EventEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    BAYROL_DEVICE_ID,
    BAYROL_DEVICE_TYPE,
    BAYROL_MESSAGE_EVENT,
    DOMAIN,
)
from .helpers import normalize_entity_id_part
from .sensor import MESSAGE_DEFINITIONS

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Bayrol message event entity."""
    # Messages (topic 10) are only published by the Automatic series.
    if config_entry.data[BAYROL_DEVICE_TYPE] not in (
        "Automatic SALT",
        "Automatic Cl-pH",
    ):
        return

    async_add_entities([BayrolMessageEventEntity(config_entry)])


class BayrolMessageEventEntity(EventEntity):
    """Records each PoolAccess message as a timestamped event."""

    _attr_name = "Message"
    _attr_icon = "mdi:message-flash"
    _attr_should_poll = False
    _attr_event_types = sorted(
        {key for key, _type, _text in MESSAGE_DEFINITIONS.values()}
    )

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize the message event entity."""
        self._config_entry = config_entry
        self._attr_unique_id = f"{config_entry.entry_id}_message_event"
        device_id = normalize_entity_id_part(config_entry.data[BAYROL_DEVICE_ID])
        self.entity_id = f"event.bayrol_{device_id}_message"

    async def async_added_to_hass(self) -> None:
        """Subscribe to bayrol_message events fired by the Messages sensor."""
        self.async_on_remove(
            self.hass.bus.async_listen(BAYROL_MESSAGE_EVENT, self._handle_bus_event)
        )

    @callback
    def _handle_bus_event(self, event: Event) -> None:
        """Record a message event belonging to this config entry."""
        if event.data.get("entry_id") != self._config_entry.entry_id:
            return
        key = event.data.get("key")
        if key not in self._attr_event_types:
            _LOGGER.debug("Skipping unknown message key: %s", key)
            return
        self._trigger_event(
            key,
            {
                "code": event.data.get("code"),
                "type": event.data.get("type"),
                "message": event.data.get("message"),
            },
        )
        self.async_write_ha_state()

    @property
    def device_info(self) -> DeviceInfo:
        """Device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._config_entry.data[BAYROL_DEVICE_ID])},
            manufacturer="Bayrol",
        )
