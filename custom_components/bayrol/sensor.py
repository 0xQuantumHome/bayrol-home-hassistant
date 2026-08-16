"""Support for Bayrol sensors."""

from __future__ import annotations

import logging
from typing import Any

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
    BAYROL_DEVICE_ID,
    BAYROL_DEVICE_TYPE,
)
from .helpers import normalize_entity_id_part

_LOGGER = logging.getLogger(__name__)

MESSAGE_TOPIC = "10"

# Topic 10 is the current message list shown by the PoolAccess application.
# Keep the stable keys from bayrol-poolaccess-mqtt so existing automations can
# continue to match them after migrating to this integration.
MESSAGE_DEFINITIONS = {
    "8.5": (
        "al_no_flow_bnc",
        "warning",
        "Filter pump off (no signal from paddle switch)",
    ),
    "8.6": (
        "al_no_flow_230V",
        "warning",
        "Filter pump off (no 230V signal from the filter pump)",
    ),
    "8.7": ("al_start_delay", "info", "Start delay"),
    "8.8": (
        "al_se_gas_detected",
        "warning",
        "Gas detected in the cell; salt electrolysis stopped",
    ),
    "8.9": (
        "al_se_err_setpoint_safe_mode",
        "warning",
        "Redox has been too low for several days; salt electrolysis is in Safe Mode",
    ),
    "8.10": (
        "al_se_err_setpoint_stopped",
        "warning",
        "Redox has been too low for several days; salt electrolysis stopped",
    ),
    "8.11": (
        "al_se_err_setpoint",
        "warning",
        "Redox has been too low for several days",
    ),
    "8.12": (
        "al_se_err_rise_safe_mode",
        "warning",
        "Redox is not rising as expected; salt electrolysis is in Safe Mode",
    ),
    "8.13": (
        "al_se_err_rise_stopped",
        "warning",
        "Redox is not rising as expected; salt electrolysis stopped",
    ),
    "8.14": ("al_se_err_rise", "warning", "Redox is not rising as expected"),
    "8.15": (
        "al_ph_dosing_stopped",
        "warning",
        "pH is not reacting as expected; pH dosing stopped",
    ),
    "8.16": (
        "al_mv_dosing_stopped",
        "warning",
        "Redox is not reacting as expected; chlorine dosing stopped",
    ),
    "8.17": ("al_ph_minus_empty", "warning", "pH-Minus canister empty"),
    "8.18": ("al_ph_plus_empty", "warning", "pH-Plus canister empty"),
    "8.19": (
        "al_salt_low_stopped",
        "warning",
        "Salt level too low; salt electrolysis stopped",
    ),
    "8.20": (
        "al_salt_low_cell_protection",
        "warning",
        "Salt level too low; cell protection mode is active",
    ),
    "8.21": ("al_salt_low_pre_warning", "warning", "Salt level below preferred level"),
    "8.22": ("al_se_production_low", "warning", "Salt electrolysis production too low"),
    "8.23": ("al_ph_too_high", "warning", "pH reading too high"),
    "8.24": ("al_ph_too_low", "warning", "pH reading too low"),
    "8.25": (
        "al_se_t_low_stopped",
        "warning",
        "Water temperature too low; salt electrolysis stopped",
    ),
    "8.26": (
        "al_se_t_low_stopped_user",
        "warning",
        "Water temperature low; salt electrolysis stopped",
    ),
    "8.27": (
        "al_se_t_low_cell_protection",
        "warning",
        "Water temperature too low; cell protection mode is active",
    ),
    "8.28": ("al_mv_too_high", "warning", "Redox reading too high"),
    "8.29": ("al_mv_too_low", "warning", "Redox reading too low"),
    "8.30": ("al_se_no_current", "warning", "No cell current"),
    "8.31": (
        "al_filtration_short",
        "warning",
        "Daily filtration time may be too short",
    ),
    "8.32": ("al_cl_empty", "warning", "Chlorine canister empty"),
    "8.33": ("enjoy", "success", "Everything is OK. Enjoy your pool!"),
    "8.34": ("ev_sw_reset", "warning", "Software reset"),
    "8.35": ("ev_system_start", "info", "Power on"),
    "8.36": ("ev_default_reset", "info", "Default reset"),
}

MESSAGE_TRANSLATIONS = {
    "fr": {
        "al_no_flow_bnc": "Pompe de filtration arrêtée (pas de débit)",
        "al_no_flow_230V": (
            "Pompe de filtration arrêtée "
            "(pas de signal 230V~ de la pompe de filtration)"
        ),
        "al_start_delay": "Délai de démarrage",
        "al_se_gas_detected": (
            "Gaz détecté dans la cellule ; électrolyse de sel arrêtée"
        ),
        "al_se_err_setpoint_safe_mode": (
            "Mesure redox trop basse depuis plusieurs jours ; "
            "électrolyse en mode Safe"
        ),
        "al_se_err_setpoint_stopped": (
            "Mesure redox trop basse depuis plusieurs jours ; électrolyse arrêtée"
        ),
        "al_se_err_setpoint": (
            "Mesure redox trop basse depuis plusieurs jours"
        ),
        "al_se_err_rise_safe_mode": (
            "La mesure redox n'augmente pas comme prévu ; "
            "électrolyse en mode Safe"
        ),
        "al_se_err_rise_stopped": (
            "La mesure redox n'augmente pas comme prévu ; électrolyse arrêtée"
        ),
        "al_se_err_rise": "La mesure redox n'augmente pas comme prévu",
        "al_ph_dosing_stopped": (
            "La mesure pH ne réagit pas comme prévu ; dosage pH arrêté"
        ),
        "al_mv_dosing_stopped": (
            "La mesure redox ne réagit pas comme prévu ; dosage chlore arrêté"
        ),
        "al_ph_minus_empty": "Bidon de pH-Minus vide",
        "al_ph_plus_empty": "Bidon de pH-Plus vide",
        "al_salt_low_stopped": (
            "Taux de sel trop bas ; électrolyse arrêtée"
        ),
        "al_salt_low_cell_protection": (
            "Taux de sel trop faible ; production réduite (protection cellule)"
        ),
        "al_salt_low_pre_warning": "Taux de sel inférieur au taux préféré",
        "al_se_production_low": "Production par électrolyse trop faible",
        "al_ph_too_high": "Mesure pH trop haute",
        "al_ph_too_low": "Mesure pH trop basse",
        "al_se_t_low_stopped": (
            "Température de l'eau trop basse ; électrolyse arrêtée"
        ),
        "al_se_t_low_stopped_user": (
            "Température de l'eau basse ; électrolyse arrêtée"
        ),
        "al_se_t_low_cell_protection": (
            "Température de l'eau trop basse ; "
            "production réduite (protection cellule)"
        ),
        "al_mv_too_high": "Mesure redox trop haute",
        "al_mv_too_low": "Mesure redox trop basse",
        "al_se_no_current": "Pas de courant cellule",
        "al_filtration_short": (
            "Temps de filtration journalier potentiellement trop faible"
        ),
        "al_cl_empty": "Bidon de Chloriliquide vide",
        "enjoy": "Tout va bien. Profitez de votre piscine !",
        "ev_sw_reset": "Réinitialisation logicielle",
        "ev_system_start": "Mise sous tension",
        "ev_default_reset": "Réinitialisation des paramètres par défaut",
    }
}


def _handle_sensor_value(sensor, value):
    """Handle incoming sensor value."""
    _LOGGER.debug(
        "Received MQTT value: %s for sensor: %s (topic %s)",
        value,
        sensor._attr_name,
        sensor._state_topic,
    )
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
                sensor._attr_native_value = "No"
            case "19.19":
                sensor._attr_native_value = "Off"
            case "19.55":
                sensor._attr_native_value = "OFF"
            case "19.95":
                sensor._attr_native_value = "Filtration is off"
            case "19.96":
                sensor._attr_native_value = "Filtration is on"
            case "19.105":
                sensor._attr_native_value = "Water detected"
            case "19.106":
                sensor._attr_native_value = "Constant production"
            case "19.115":
                sensor._attr_native_value = "Auto Plus"
            case "19.142":
                sensor._attr_native_value = "Open"
            case "19.143":
                sensor._attr_native_value = "Closed"
            case "19.147":
                sensor._attr_native_value = "Stopped (gas detected)"
            case "19.176":
                sensor._attr_native_value = "Off"
            case "19.177":
                sensor._attr_native_value = "On"
            case "19.195":
                sensor._attr_native_value = "Auto"
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
            case 7003:
                sensor._attr_native_value = "Yes"
            case 7004:
                sensor._attr_native_value = "No"
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

    if device_type == "Automatic SALT":
        for sensor_type, sensor_config in SENSOR_TYPES_AUTOMATIC_SALT.items():
            if sensor_config.get("entity_type") not in (
                "select",
                "number",
                "switch",
            ):  # Skip writable entities
                topic = sensor_type
                sensor = BayrolSensor(config_entry, sensor_type, sensor_config, topic)
                mqtt_manager.subscribe(
                    topic, lambda v, s=sensor: _handle_sensor_value(s, v)
                )
                entities.append(sensor)
    elif device_type == "Automatic Cl-pH":
        for sensor_type, sensor_config in SENSOR_TYPES_AUTOMATIC_CL_PH.items():
            if sensor_config.get("entity_type") not in (
                "select",
                "number",
                "switch",
            ):  # Skip writable entities
                topic = sensor_type
                sensor = BayrolSensor(config_entry, sensor_type, sensor_config, topic)
                mqtt_manager.subscribe(
                    topic, lambda v, s=sensor: _handle_sensor_value(s, v)
                )
                entities.append(sensor)
    elif device_type == "PM5 Chlorine":
        for sensor_type, sensor_config in SENSOR_TYPES_PM5_CHLORINE.items():
            if sensor_config.get("entity_type") not in (
                "select",
                "number",
                "switch",
            ):  # Skip writable entities
                topic = sensor_type
                sensor = BayrolSensor(config_entry, sensor_type, sensor_config, topic)
                mqtt_manager.subscribe(
                    topic, lambda v, s=sensor: _handle_sensor_value(s, v)
                )
                entities.append(sensor)

    if device_type in ("Automatic SALT", "Automatic Cl-pH"):
        messages = BayrolMessagesSensor(config_entry, hass.config.language)
        mqtt_manager.subscribe(MESSAGE_TOPIC, messages.handle_message_payload)
        entities.append(messages)

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
            self._attr_suggested_display_precision = 2
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


class BayrolMessagesSensor(SensorEntity):
    """Current PoolAccess messages published on MQTT topic 10."""

    _attr_name = "Messages"
    _attr_icon = "mdi:message-bulleted"
    _attr_should_poll = False

    def __init__(self, config_entry: ConfigEntry, language: str) -> None:
        """Initialize the messages sensor."""
        self._config_entry = config_entry
        self._language = (
            language.lower().replace("_", "-").split("-", maxsplit=1)[0]
        )
        self._message_language = (
            self._language if self._language in MESSAGE_TRANSLATIONS else "en"
        )
        self._attr_unique_id = f"{config_entry.entry_id}_{MESSAGE_TOPIC}"
        device_id = normalize_entity_id_part(config_entry.data[BAYROL_DEVICE_ID])
        self.entity_id = f"sensor.bayrol_{device_id}_messages"
        self._attr_native_value = None
        self._message_codes: list[str] = []
        self._messages: list[dict[str, str]] = []

    def handle_message_payload(self, payload: Any) -> None:
        """Decode the current PoolAccess message list."""
        if payload is None:
            raw_codes = []
        elif isinstance(payload, (list, tuple)):
            raw_codes = list(payload)
        elif isinstance(payload, (str, int, float)):
            raw_codes = [payload]
        else:
            _LOGGER.warning(
                "Unexpected MQTT payload type for Bayrol messages: %s",
                type(payload),
            )
            return

        self._message_codes = [self._normalize_message_code(code) for code in raw_codes]
        self._messages = [self._message_details(code) for code in self._message_codes]

        keys = [message["key"] for message in self._messages]
        state = ", ".join(keys) if keys else "none"
        self._attr_native_value = (
            state if len(state) <= 255 else f"{len(keys)} messages"
        )
        self._attr_icon = (
            "mdi:message-alert"
            if any(message["type"] == "warning" for message in self._messages)
            else "mdi:message-bulleted"
        )

        if self.hass is not None:
            self.schedule_update_ha_state()

    @staticmethod
    def _normalize_message_code(value: Any) -> str:
        """Normalize a message code, including numeric JSON values."""
        code = str(value)
        if code in MESSAGE_DEFINITIONS:
            return code

        try:
            numeric_code = float(code)
        except (TypeError, ValueError):
            return code

        # Numeric JSON payloads lose trailing zeros ("8.30" arrives as 8.3),
        # so codes are matched by float value. This is unambiguous as long as
        # no two known codes share the same float (e.g. "8.3" vs "8.30");
        # currently codes 8.1 to 8.4 do not exist. Warn if that ever changes.
        matches = [
            known_code
            for known_code in MESSAGE_DEFINITIONS
            if float(known_code) == numeric_code
        ]
        if len(matches) > 1:
            _LOGGER.warning(
                "Ambiguous Bayrol message code %s matches %s; using %s",
                code,
                matches,
                matches[0],
            )
        return matches[0] if matches else code

    def _message_details(self, code: str) -> dict[str, str]:
        """Return stable metadata for one PoolAccess message code."""
        definition = MESSAGE_DEFINITIONS.get(code)
        if definition is None:
            return {
                "code": code,
                "key": f"unknown_{code.replace('.', '_')}",
                "type": "unknown",
                "message": (
                    f"Message Bayrol inconnu ({code})"
                    if self._message_language == "fr"
                    else f"Unknown Bayrol message ({code})"
                ),
            }

        key, message_type, message = definition
        message = MESSAGE_TRANSLATIONS.get(self._message_language, {}).get(
            key, message
        )
        return {
            "code": code,
            "key": key,
            "type": message_type,
            "message": message,
        }

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the raw codes and decoded messages."""
        message_keys = [message["key"] for message in self._messages]
        return {
            "message_codes": self._message_codes,
            "message_keys": message_keys,
            "message_language": self._message_language,
            "data": self._messages,
        }

    @property
    def device_info(self) -> DeviceInfo:
        """Return the Bayrol device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._config_entry.data[BAYROL_DEVICE_ID])},
            manufacturer="Bayrol",
        )
