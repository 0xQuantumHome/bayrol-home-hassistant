"""Button platform for quitting Bayrol device alarms."""

from __future__ import annotations

import json
import logging

from homeassistant.components.button import ButtonDeviceClass, ButtonEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    DOMAIN,
    BAYROL_DEVICE_ID,
)
from .helpers import normalize_entity_id_part

_LOGGER = logging.getLogger(__name__)

# The topic that requires acknowledgement
QUIT_ALARM_TOPIC = "8.2002"


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Bayrol quit alarm button."""
    async_add_entities([BayrolQuitAlarmButton(config_entry)])


class BayrolQuitAlarmButton(ButtonEntity):
    """
    Button that acknowledges (quits) an active Bayrol device alarm.

    When pressed, publishes a quit command to d02/{serial}/s/8.2002.
    The device will respond on v/8.2002 with is_quit=true, active=false,
    which the binary_sensor will pick up and turn off.

    Note: the exact quit payload format ({"t":"8.2002","v":1}) is an
    educated guess based on how other Bayrol set commands work.
    If the device does not respond, the payload may need adjustment.
    """

    _attr_device_class = ButtonDeviceClass.RESTART
    _attr_should_poll = False

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialise the quit alarm button."""
        self._config_entry = config_entry
        device_id = normalize_entity_id_part(config_entry.data[BAYROL_DEVICE_ID])

        self._attr_name = "Quit Alarm"
        self._attr_unique_id = f"{config_entry.entry_id}_quit_alarm"
        self.entity_id = f"button.bayrol_{device_id}_quit_alarm"

    async def async_press(self) -> None:
        """Publish the alarm quit command to the device."""
        device_id = self._config_entry.data[BAYROL_DEVICE_ID]
        topic = f"d02/{device_id}/s/{QUIT_ALARM_TOPIC}"
        # Quit payload mirrors the set-command pattern used by select entities.
        # v=1 signals the device to acknowledge and clear the alarm.
        payload = json.dumps({"t": QUIT_ALARM_TOPIC, "v": 1})

        mqtt_manager = self.hass.data[DOMAIN][self._config_entry.entry_id][
            "mqtt_manager"
        ]

        if not mqtt_manager.client or not mqtt_manager.client.is_connected():
            _LOGGER.warning("Cannot quit alarm: MQTT client is not connected")
            return

        mqtt_manager.client.publish(topic, payload)
        _LOGGER.info("Published alarm quit command to %s: %s", topic, payload)

    @property
    def device_info(self) -> DeviceInfo:
        """Link this button to the Bayrol device."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._config_entry.data[BAYROL_DEVICE_ID])},
            manufacturer="Bayrol",
        )
