"""Support for Bayrol select entities."""

from __future__ import annotations

import logging
import json

from homeassistant.components.select import SelectEntity
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
    AUTOMATIC_MQTT_TO_TEXT_MAPPING,
    PM5_MQTT_TO_TEXT_MAPPING,
    AUTOMATIC_TEXT_TO_MQTT_MAPPING,
    PM5_TEXT_TO_MQTT_MAPPING,
)

_LOGGER = logging.getLogger(__name__)


def _handle_select_value(select, value):
    """Handle incoming select value."""
    _LOGGER.debug("Received MQTT value: %s for select: %s", value, select._attr_name)
    _LOGGER.debug("Available options: %s", select._attr_options)
    
    # Try to find the value in the device-specific mappings
    if select._config_entry.data[BAYROL_DEVICE_TYPE] == "PM5 Chlorine":
        if str(value) in PM5_MQTT_TO_TEXT_MAPPING:
            select._attr_current_option = PM5_MQTT_TO_TEXT_MAPPING[str(value)]
            _LOGGER.debug("PM5 mapping found: %s -> %s", value, select._attr_current_option)
        else:
            # Try coefficient conversion for numeric values
            _handle_numeric_value(select, value)
    elif (select._config_entry.data[BAYROL_DEVICE_TYPE] == "Automatic Cl-pH" or 
          select._config_entry.data[BAYROL_DEVICE_TYPE] == "Automatic SALT"):
        if str(value) in AUTOMATIC_MQTT_TO_TEXT_MAPPING:
            select._attr_current_option = AUTOMATIC_MQTT_TO_TEXT_MAPPING[str(value)]
            _LOGGER.debug("Automatic mapping found: %s -> %s", value, select._attr_current_option)
        else:
            # Try coefficient conversion for numeric values
            _handle_numeric_value(select, value)
    else:
        _LOGGER.warning("Unknown device type: %s", select._config_entry.data[BAYROL_DEVICE_TYPE])
        _handle_numeric_value(select, value)
    
    _LOGGER.debug("Set current_option to: %s", select._attr_current_option)
    select.schedule_update_ha_state()


def _handle_numeric_value(select, value):
    """Handle numeric values using coefficient conversion."""
    try:
        coefficient = select._select_config.get("coefficient")
        if coefficient is not None and coefficient != -1:
            converted_value = float(value) / coefficient
            _LOGGER.debug("Converted value using coefficient %s: %s -> %s", coefficient, value, converted_value)
            
            # Find the closest option
            if coefficient == 1:
                converted_value = int(converted_value)
                options = [int(opt) for opt in select._attr_options]
            else:
                converted_value = float(converted_value)
                options = [float(opt) for opt in select._attr_options]
            
            closest_option = min(options, key=lambda x: abs(x - converted_value))
            select._attr_current_option = str(closest_option)
            _LOGGER.debug("Found closest option: %s", closest_option)
        else:
            # No coefficient, use value directly
            select._attr_current_option = str(value)
    except (ValueError, TypeError) as e:
        _LOGGER.warning("Error converting value %s: %s", value, e)
        select._attr_current_option = str(value)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Bayrol select entities."""
    entities = []
    device_type = config_entry.data[BAYROL_DEVICE_TYPE]
    _LOGGER.debug("device_type: %s", device_type)

    # Get the shared MQTT manager
    mqtt_manager = hass.data[DOMAIN]["mqtt_manager"]

    if device_type == "Automatic SALT":
        for select_type, select_config in SENSOR_TYPES_AUTOMATIC_SALT.items():
            if select_config.get("entity_type") == "select":
                topic = select_type
                select = BayrolSelect(config_entry, select_type, select_config, topic)
                mqtt_manager.subscribe(
                    topic, lambda v, s=select: _handle_select_value(s, v)
                )
                entities.append(select)
    elif device_type == "Automatic Cl-pH":
        for select_type, select_config in SENSOR_TYPES_AUTOMATIC_CL_PH.items():
            if select_config.get("entity_type") == "select":
                topic = select_type
                select = BayrolSelect(config_entry, select_type, select_config, topic)
                mqtt_manager.subscribe(
                    topic, lambda v, s=select: _handle_select_value(s, v)
                )
                entities.append(select)
    elif device_type == "PM5 Chlorine":
        for select_type, select_config in SENSOR_TYPES_PM5_CHLORINE.items():
            if select_config.get("entity_type") == "select":
                topic = select_type
                select = BayrolSelect(config_entry, select_type, select_config, topic)
                mqtt_manager.subscribe(
                    topic, lambda v, s=select: _handle_select_value(s, v)
                )
                entities.append(select)

    async_add_entities(entities)


class BayrolSelect(SelectEntity):
    """Representation of a Bayrol select entity."""

    def __init__(self, config_entry, select_type, select_config, topic):
        """Initialize the select entity."""
        self._config_entry = config_entry
        self._select_type = select_type
        self._select_config = select_config
        self._state_topic = topic
        self._attr_name = select_config.get("name", select_type)
        self._attr_unique_id = f"{config_entry.entry_id}_{select_type}"
        self.entity_id = (
            "select.bayrol_"
            + config_entry.data[BAYROL_DEVICE_ID]
            + "_"
            + select_config.get("name", select_type)
        )
        self._attr_current_option = None

        # Get options from config and convert to strings
        self._attr_options = [str(opt) for opt in select_config.get("options", [])]

        # Create custom mappings if provided
        self._mqtt_to_value = {}
        if "mqtt_values" in select_config:
            self._mqtt_to_value = select_config["mqtt_values"]

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        _LOGGER.debug("User selected option: %s", option)
        
        # Convert display text back to MQTT value based on device type
        mqtt_value = None
        
        if self._config_entry.data[BAYROL_DEVICE_TYPE] == "PM5 Chlorine":
            # Use PM5 specific mappings
            if option in PM5_TEXT_TO_MQTT_MAPPING:
                mqtt_value = PM5_TEXT_TO_MQTT_MAPPING[option]
                _LOGGER.debug("PM5 text mapping: %s -> %s", option, mqtt_value)
        elif (self._config_entry.data[BAYROL_DEVICE_TYPE] == "Automatic Cl-pH" or 
              self._config_entry.data[BAYROL_DEVICE_TYPE] == "Automatic SALT"):
            # Use Automatic specific mappings
            if option in AUTOMATIC_TEXT_TO_MQTT_MAPPING:
                mqtt_value = AUTOMATIC_TEXT_TO_MQTT_MAPPING[option]
                _LOGGER.debug("Automatic text mapping: %s -> %s", option, mqtt_value)
        
        if mqtt_value is None:
            # If no text mapping found, try coefficient conversion for numeric options
            try:
                coefficient = self._select_config.get("coefficient")
                if coefficient is not None and coefficient != -1:
                    # Convert display value to MQTT value
                    display_float = float(option)
                    mqtt_value = str(int(display_float * coefficient))
                    _LOGGER.debug("Converted display value %s to MQTT value %s using coefficient %s", 
                                option, mqtt_value, coefficient)
                else:
                    # No coefficient, use option as MQTT value directly
                    mqtt_value = option
                    _LOGGER.debug("Using option as MQTT value directly: %s", mqtt_value)
            except (ValueError, TypeError) as e:
                _LOGGER.error("Error converting option %s to MQTT value: %s", option, e)
                return

        # Verify the option is valid
        # For text mappings, check if the MQTT value is in options
        # For numeric options, check if the original option is in options
        if mqtt_value in self._attr_options:
            # This is a text mapping case (like Production Rate)
            _LOGGER.debug("Text mapping case: MQTT value %s found in options", mqtt_value)
        elif option in self._attr_options:
            # This is a numeric case (like Salt Level)
            _LOGGER.debug("Numeric case: option %s found in options", option)
        else:
            _LOGGER.error("Invalid option: %s (MQTT value: %s). Available options: %s", 
                         option, mqtt_value, self._attr_options)
            return

        # Update the current option to the MQTT value
        self._attr_current_option = mqtt_value

        # Publish the new value to the MQTT topic
        topic = f"d02/{self._config_entry.data[BAYROL_DEVICE_ID]}/s/{self._state_topic}"
        payload = f'{{"t":"{self._state_topic}","v":{mqtt_value}}}'
        self.hass.data[DOMAIN]["mqtt_manager"].client.publish(topic, payload)
        _LOGGER.debug("Published MQTT message: %s", payload)

    @property
    def options(self) -> list[str]:
        """Return a list of available options."""
        # Convert MQTT values to display text based on device type
        display_options = []
        for option in self._attr_options:
            # Convert option to string for mapping lookup
            option_str = str(option)
            
            if self._config_entry.data[BAYROL_DEVICE_TYPE] == "PM5 Chlorine":
                # Use PM5 specific mappings
                if option_str in PM5_MQTT_TO_TEXT_MAPPING:
                    display_options.append(PM5_MQTT_TO_TEXT_MAPPING[option_str])
                else:
                    display_options.append(option_str)
            elif (self._config_entry.data[BAYROL_DEVICE_TYPE] == "Automatic Cl-pH" or 
                  self._config_entry.data[BAYROL_DEVICE_TYPE] == "Automatic SALT"):
                # Use Automatic specific mappings
                if option_str in AUTOMATIC_MQTT_TO_TEXT_MAPPING:
                    display_options.append(AUTOMATIC_MQTT_TO_TEXT_MAPPING[option_str])
                else:
                    display_options.append(option_str)
            else:
                # Unknown device type - this should not happen
                _LOGGER.warning("Unknown device type: %s. Cannot map option: %s", 
                               self._config_entry.data[BAYROL_DEVICE_TYPE], option_str)
                display_options.append(option_str)
        return display_options

    @property
    def current_option(self) -> str | None:
        """Return the currently selected option."""
        if self._attr_current_option is None:
            return None
        
        _LOGGER.debug("Converting MQTT value %s to display text for device type: %s", 
                     self._attr_current_option, self._config_entry.data[BAYROL_DEVICE_TYPE])
        
        # Convert MQTT value to display text based on device type
        if self._config_entry.data[BAYROL_DEVICE_TYPE] == "PM5 Chlorine":
            # Use PM5 specific mappings
            if self._attr_current_option in PM5_MQTT_TO_TEXT_MAPPING:
                result = PM5_MQTT_TO_TEXT_MAPPING[self._attr_current_option]
                _LOGGER.debug("PM5 mapping: %s -> %s", self._attr_current_option, result)
                return result
        elif (self._config_entry.data[BAYROL_DEVICE_TYPE] == "Automatic Cl-pH" or 
              self._config_entry.data[BAYROL_DEVICE_TYPE] == "Automatic SALT"):
            # Use Automatic specific mappings
            if self._attr_current_option in AUTOMATIC_MQTT_TO_TEXT_MAPPING:
                result = AUTOMATIC_MQTT_TO_TEXT_MAPPING[self._attr_current_option]
                _LOGGER.debug("Automatic mapping: %s -> %s", self._attr_current_option, result)
                return result
        else:
            # Unknown device type - this should not happen
            _LOGGER.warning("Unknown device type: %s. Cannot map MQTT value: %s", 
                           self._config_entry.data[BAYROL_DEVICE_TYPE], self._attr_current_option)
            return self._attr_current_option
        
        # This line is reached when device type is known but MQTT value not found in mapping
        _LOGGER.debug("No mapping found for MQTT value %s in device type %s, returning original value", 
                     self._attr_current_option, self._config_entry.data[BAYROL_DEVICE_TYPE])
        return self._attr_current_option

    @property
    def device_info(self) -> DeviceInfo:
        """Device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._config_entry.data[BAYROL_DEVICE_ID])},
            manufacturer="Bayrol",
        )