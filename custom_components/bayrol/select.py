"""Support for Bayrol select entities."""

from __future__ import annotations

import logging

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
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
from .helpers import normalize_entity_id_part
from .pump import get_pump_setup

_LOGGER = logging.getLogger(__name__)


def _handle_select_value(select, value):
    """Handle incoming select value."""
    _LOGGER.debug("Received MQTT value: %s for select: %s", value, select._attr_name)
    _LOGGER.debug("Available options: %s", select._attr_options)

    # Prefer a topic-specific mapping when one is configured.
    if str(value) in select._mqtt_to_value:
        select._attr_current_option = select._mqtt_to_value[str(value)]
        _LOGGER.debug(
            "Topic-specific mapping found: %s -> %s",
            value,
            select._attr_current_option,
        )
    # Otherwise use the device-specific mappings and store the TEXT value.
    elif select._config_entry.data[BAYROL_DEVICE_TYPE] == "PM5 Chlorine":
        if str(value) in PM5_MQTT_TO_TEXT_MAPPING:
            select._attr_current_option = PM5_MQTT_TO_TEXT_MAPPING[str(value)]
            _LOGGER.debug(
                "PM5 mapping found: %s -> %s", value, select._attr_current_option
            )
        else:
            # Try coefficient conversion for numeric values
            _handle_numeric_value(select, value)
    elif (
        select._config_entry.data[BAYROL_DEVICE_TYPE] == "Automatic Cl-pH"
        or select._config_entry.data[BAYROL_DEVICE_TYPE] == "Automatic SALT"
    ):
        if str(value) in AUTOMATIC_MQTT_TO_TEXT_MAPPING:
            select._attr_current_option = AUTOMATIC_MQTT_TO_TEXT_MAPPING[str(value)]
            _LOGGER.debug(
                "Automatic mapping found: %s -> %s", value, select._attr_current_option
            )
        else:
            # Try coefficient conversion for numeric values
            _handle_numeric_value(select, value)
    else:
        _LOGGER.warning(
            "Unknown device type: %s", select._config_entry.data[BAYROL_DEVICE_TYPE]
        )
        _handle_numeric_value(select, value)

    _LOGGER.debug("Set current_option to: %s", select._attr_current_option)
    if select.hass is not None:
        select.schedule_update_ha_state()


def _handle_numeric_value(select, value):
    """Handle numeric values using coefficient conversion."""
    try:
        coefficient = select._select_config.get("coefficient")
        if coefficient is not None and coefficient != -1:
            converted_value = float(value) / coefficient
            _LOGGER.debug(
                "Converted value using coefficient %s: %s -> %s",
                coefficient,
                value,
                converted_value,
            )

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

    # Get the MQTT manager for this specific config entry
    mqtt_manager = hass.data[DOMAIN][config_entry.entry_id]["mqtt_manager"]

    if device_type == "Automatic SALT":
        for select_type, select_config in SENSOR_TYPES_AUTOMATIC_SALT.items():
            if select_config.get("filtration"):
                entities.append(
                    BayrolFiltrationSelect(
                        config_entry, select_type, select_config, mqtt_manager,
                        get_pump_setup(hass, config_entry, SENSOR_TYPES_AUTOMATIC_SALT),
                    )
                )
            elif select_config.get("entity_type") == "select":
                topic = select_type
                select = BayrolSelect(config_entry, select_type, select_config, topic)
                mqtt_manager.subscribe(
                    topic, lambda v, s=select: _handle_select_value(s, v)
                )
                entities.append(select)
    elif device_type == "Automatic Cl-pH":
        for select_type, select_config in SENSOR_TYPES_AUTOMATIC_CL_PH.items():
            if select_config.get("filtration"):
                entities.append(
                    BayrolFiltrationSelect(
                        config_entry, select_type, select_config, mqtt_manager,
                        get_pump_setup(hass, config_entry, SENSOR_TYPES_AUTOMATIC_CL_PH),
                    )
                )
            elif select_config.get("entity_type") == "select":
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

    _attr_should_poll = False

    def __init__(self, config_entry, select_type, select_config, topic):
        """Initialize the select entity."""
        self._config_entry = config_entry
        self._select_type = select_type
        self._select_config = select_config
        self._state_topic = topic
        self._attr_name = select_config.get("name", select_type)
        self._attr_unique_id = f"{config_entry.entry_id}_{select_type}"
        device_id = normalize_entity_id_part(config_entry.data[BAYROL_DEVICE_ID])
        name = normalize_entity_id_part(select_config.get("name", select_type))
        self.entity_id = f"select.bayrol_{device_id}_{name}"
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

        # Prefer a topic-specific mapping when one is configured.
        if self._mqtt_to_value:
            value_to_mqtt = {
                display_value: mapped_mqtt_value
                for mapped_mqtt_value, display_value in self._mqtt_to_value.items()
            }
            mqtt_value = value_to_mqtt.get(option)
            if mqtt_value is not None:
                _LOGGER.debug(
                    "Topic-specific text mapping: %s -> %s", option, mqtt_value
                )

        if (
            mqtt_value is None
            and self._config_entry.data[BAYROL_DEVICE_TYPE] == "PM5 Chlorine"
        ):
            # Use PM5 specific mappings
            if option in PM5_TEXT_TO_MQTT_MAPPING:
                mqtt_value = PM5_TEXT_TO_MQTT_MAPPING[option]
                _LOGGER.debug("PM5 text mapping: %s -> %s", option, mqtt_value)
        elif (
            mqtt_value is None
            and (
                self._config_entry.data[BAYROL_DEVICE_TYPE] == "Automatic Cl-pH"
                or self._config_entry.data[BAYROL_DEVICE_TYPE] == "Automatic SALT"
            )
        ):
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
                    mqtt_value = str(round(display_float * coefficient))
                    _LOGGER.debug(
                        "Converted display value %s to MQTT value %s using coefficient %s",
                        option,
                        mqtt_value,
                        coefficient,
                    )
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
            _LOGGER.debug(
                "Text mapping case: MQTT value %s found in options", mqtt_value
            )
        elif option in self._attr_options:
            # This is a numeric case (like Salt Level)
            _LOGGER.debug("Numeric case: option %s found in options", option)
        else:
            _LOGGER.error(
                "Invalid option: %s (MQTT value: %s). Available options: %s",
                option,
                mqtt_value,
                self._attr_options,
            )
            return

        self.hass.data[DOMAIN][self._config_entry.entry_id][
            "mqtt_manager"
        ].set_value(self._state_topic, mqtt_value)

    @property
    def options(self) -> list[str]:
        """Return a list of available options."""
        # Convert MQTT values to display text based on device type
        display_options = []
        for option in self._attr_options:
            # Convert option to string for mapping lookup
            option_str = str(option)

            if option_str in self._mqtt_to_value:
                # Prefer a topic-specific mapping when one is configured
                display_options.append(self._mqtt_to_value[option_str])
            elif self._config_entry.data[BAYROL_DEVICE_TYPE] == "PM5 Chlorine":
                # Use PM5 specific mappings
                if option_str in PM5_MQTT_TO_TEXT_MAPPING:
                    display_options.append(PM5_MQTT_TO_TEXT_MAPPING[option_str])
                else:
                    display_options.append(option_str)
            elif (
                self._config_entry.data[BAYROL_DEVICE_TYPE] == "Automatic Cl-pH"
                or self._config_entry.data[BAYROL_DEVICE_TYPE] == "Automatic SALT"
            ):
                # Use Automatic specific mappings
                if option_str in AUTOMATIC_MQTT_TO_TEXT_MAPPING:
                    display_options.append(AUTOMATIC_MQTT_TO_TEXT_MAPPING[option_str])
                else:
                    display_options.append(option_str)
            else:
                # Unknown device type - this should not happen
                _LOGGER.warning(
                    "Unknown device type: %s. Cannot map option: %s",
                    self._config_entry.data[BAYROL_DEVICE_TYPE],
                    option_str,
                )
                display_options.append(option_str)
        return display_options

    @property
    def device_info(self) -> DeviceInfo:
        """Device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._config_entry.data[BAYROL_DEVICE_ID])},
            manufacturer="Bayrol",
        )


class BayrolFiltrationSelect(SelectEntity):
    """Filtration mode, written to the datapoint matching the pump setup.

    Unavailable while the device reports no Smart&Easy filter pump (or the
    setup is not known yet). Keeps the unique_id of the former 5.184 select.
    """

    _attr_should_poll = False

    def __init__(self, config_entry, key, config, mqtt_manager, pump_setup):
        """Initialize the filtration mode select."""
        self._config_entry = config_entry
        self._mqtt_manager = mqtt_manager
        self._pump_setup = pump_setup
        self._mode_options: dict[str, dict[str, str]] = config["mode_options"]
        self._mode_values: dict[str, str] = {}
        self._attr_name = config.get("name", key)
        self._attr_unique_id = f"{config_entry.entry_id}_{key}"
        device_id = normalize_entity_id_part(config_entry.data[BAYROL_DEVICE_ID])
        name = normalize_entity_id_part(config.get("name", key))
        self.entity_id = f"select.bayrol_{device_id}_{name}"
        for topic in config["mode_topics"].values():
            mqtt_manager.subscribe(
                topic, lambda v, t=topic: self._on_mode_value(t, v)
            )
        pump_setup.add_listener(self._update_state)

    def _on_mode_value(self, topic: str, value) -> None:
        self._mode_values[topic] = str(value)
        self._update_state()

    def _update_state(self) -> None:
        if self.hass is not None:
            self.schedule_update_ha_state()

    @property
    def available(self) -> bool:
        """Only available when the device reports a filter pump setup."""
        return self._pump_setup.mode_topic is not None

    @property
    def options(self) -> list[str]:
        """Options of the active filtration mode datapoint."""
        topic = self._pump_setup.mode_topic
        if topic is None:
            return []
        return list(self._mode_options[topic].values())

    @property
    def current_option(self) -> str | None:
        """Mode reported by the device on the active datapoint."""
        topic = self._pump_setup.mode_topic
        if topic is None:
            return None
        return self._mode_options[topic].get(self._mode_values.get(topic, ""))

    @property
    def extra_state_attributes(self) -> dict[str, str | None]:
        """Expose the detected setup for diagnostics."""
        return {
            "mode_datapoint": self._pump_setup.mode_topic,
            "variable_speed_pump": self._pump_setup.vsp_used,
            "temperature_sensor": self._pump_setup.temp_used,
            "pump_output": self._pump_setup.pump_out,
        }

    async def async_select_option(self, option: str) -> None:
        """Send the mode to the active filtration mode datapoint."""
        topic = self._pump_setup.mode_topic
        if topic is None:
            raise HomeAssistantError("No Smart&Easy filter pump detected")
        codes = {text: code for code, text in self._mode_options[topic].items()}
        if option not in codes:
            raise HomeAssistantError(f"Invalid filtration mode: {option}")
        self._mqtt_manager.set_value(topic, codes[option])

    @property
    def device_info(self) -> DeviceInfo:
        """Device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._config_entry.data[BAYROL_DEVICE_ID])},
            manufacturer="Bayrol",
        )
