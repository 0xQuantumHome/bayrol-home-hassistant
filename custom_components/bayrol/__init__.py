"""The Bayrol integration."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    DOMAIN,
    BAYROL_ACCESS_TOKEN,
    BAYROL_DEVICE_ID,
)
from .mqtt_manager import BayrolMQTTManager

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Bayrol from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    # Create and store MQTT manager
    mqtt_manager = BayrolMQTTManager(
        hass, entry.data[BAYROL_DEVICE_ID], entry.data[BAYROL_ACCESS_TOKEN]
    )
    # Store mqtt_manager per entry so multiple config entries don't overwrite each other
    hass.data[DOMAIN][entry.entry_id] = {
        "data": entry.data,
        "mqtt_manager": mqtt_manager,
    }
    mqtt_manager.start()

    # Forward the setup to the platforms
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor", "select"])

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(
        entry, ["sensor", "select"]
    )

    if unload_ok:
        # Clean up only this entry's MQTT manager
        entry_data = hass.data[DOMAIN].pop(entry.entry_id, {})
        mqtt_manager = entry_data.get("mqtt_manager")
        if mqtt_manager:
            if mqtt_manager.client:
                mqtt_manager.client.disconnect()
            if mqtt_manager.thread:
                mqtt_manager.thread.join(timeout=1.0)

    return unload_ok
