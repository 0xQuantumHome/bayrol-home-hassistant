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
    BAYROL_MESSAGE_EVENT,
)
from .helpers import normalize_entity_id_part

_LOGGER = logging.getLogger(__name__)

MESSAGE_TOPIC = "10"

# Topic 10 is the current message list shown by the PoolAccess application.
# Codes, keys and texts are extracted from the official Bayrol web app
# (v1.0.147: Messages.js + MessageStringsExternal.js). Keys stay stable so
# existing automations keep matching.
MESSAGE_DEFINITIONS = {
    "8.5": ("al_no_flow_bnc", "warning", "Filter pump off (no signal from paddle switch)"),
    "8.6": ("al_no_flow_230V", "warning", "Filter pump off (no 230V~ signal from the filter pump)"),
    "8.7": ("al_start_delay", "info", "Start delay"),
    "8.8": ("al_se_gas_detected", "warning", "Gas detection in the cell ! Salt electrolysis stopped !"),
    "8.9": ("al_se_err_setpoint_safe_mode", "warning", "Redox reading too low for several days ! Salt electrolysis running in Safe Mode !"),
    "8.10": ("al_se_err_setpoint_stopped", "warning", "Redox reading too low for several days ! Salt electrolysis stopped !"),
    "8.11": ("al_se_err_setpoint", "warning", "Redox reading too low for several days"),
    "8.12": ("al_se_err_rise_safe_mode", "warning", "Redox reading does not rise as expected ! Salt electrolysis running in Safe Mode !"),
    "8.13": ("al_se_err_rise_stopped", "warning", "Redox reading does not rise as expected ! Salt electrolysis stopped !"),
    "8.14": ("al_se_err_rise", "warning", "Redox reading does not rise as expected"),
    "8.15": ("al_ph_dosing_stopped", "warning", "pH reading does not react as expected ! pH dosing stopped !"),
    "8.16": ("al_mv_dosing_stopped", "warning", "Redox reading does not react as expected ! Chlorine dosing stopped !"),
    "8.17": ("al_ph_minus_empty", "warning", "pH-Minus canister empty"),
    "8.18": ("al_ph_plus_empty", "warning", "pH-Plus canister empty"),
    "8.19": ("al_salt_low_stopped", "warning", "Salt level too low ! Salt electrolysis stopped !"),
    "8.20": ("al_salt_low_cell_protection", "warning", "Salt level too low ! Cell protection mode (low production) !"),
    "8.21": ("al_salt_low_pre_warning", "warning", "Salt level below preferred level"),
    "8.22": ("al_se_production_low", "warning", "Salt electrolysis production low"),
    "8.23": ("al_ph_too_high", "warning", "pH reading too high"),
    "8.24": ("al_ph_too_low", "warning", "pH reading too low"),
    "8.25": ("al_se_t_low_stopped", "warning", "Water temperature too low Salt electrolysis stopped"),
    "8.26": ("al_se_t_low_stopped_user", "warning", "Water temperature low Salt electrolysis stopped"),
    "8.27": ("al_se_t_low_cell_protection", "warning", "Water temperature too low Cell protection mode (low production)"),
    "8.28": ("al_mv_too_high", "warning", "Redox reading too high"),
    "8.29": ("al_mv_too_low", "warning", "Redox reading too low"),
    "8.30": ("al_se_no_current", "warning", "No cell current"),
    "8.31": ("al_filtration_short", "warning", "Daily filtration time potentially too short"),
    "8.32": ("al_cl_empty", "warning", "Chlorine canister empty"),
    "8.33": ("enjoy", "success", "Everything is OK. Enjoy your pool!"),
    "8.34": ("ev_sw_reset", "warning", "Software reset"),
    "8.35": ("ev_system_start", "info", "Power on"),
    "8.36": ("ev_default_reset", "info", "Default reset"),
    "8.37": ("al_fm_connection_lost", "warning", "Control Module: connection lost"),
    "8.38": ("al_fm_connection_unstable", "warning", "Control Module: connection unstable"),
    "8.39": ("al_sw_update_required", "warning", "Software update required"),
    "8.40": ("al_se_fault_one_polarity", "warning", "Salt electrolysis system fault (0x01R)"),
    "8.41": ("al_se_fault_voltage_ok", "warning", "Salt electrolysis: no production"),
    "8.42": ("al_se_fault_voltage_not_ok", "warning", "Salt electrolysis system fault (0x02V)"),
    "8.43": ("al_ph_dos_limit", "warning", "Daily pH dosing limit reached ! pH dosing stopped !"),
    "8.44": ("al_cl_dos_limit", "warning", "Daily chlorine dosing limit reached ! Chlorine dosing stopped !"),
    "8.45": ("al_ph_out_of_range", "warning", "pH reading out of range ! pH dosing and disinfection stopped !"),
    "8.46": ("al_mv_out_of_range", "warning", "Redox (mV) reading out of range ! Chlorine dosing stopped !"),
    "8.47": ("al_se_mv_out_of_range", "warning", "Redox (mV) reading out of range ! Salt electrolysis stopped !"),
}

MESSAGE_TRANSLATIONS = {
    "de": {
        "al_no_flow_bnc": "Filterpumpe aus (kein Signal vom Paddelschalter)",
        "al_no_flow_230V": "Filterpumpe aus (kein 230V~ Signal von der Filterpumpe)",
        "al_start_delay": "Start-Verzögerung",
        "al_se_gas_detected": "Gas in der Zelle erkannt ! Salz-Elektrolyse gestoppt !",
        "al_se_err_setpoint_safe_mode": "Redoxwert zu gering über mehrere Tage ! Salz-Elektrolyse läuft im Safe Mode !",
        "al_se_err_setpoint_stopped": "Redoxwert zu gering über mehrere Tage ! Salz-Elektrolyse gestoppt !",
        "al_se_err_setpoint": "Redoxwert zu gering über mehrere Tage",
        "al_se_err_rise_safe_mode": "Redoxwert erhöht sich nicht wie erwartet ! Salz-Elektrolyse läuft im Safe Mode !",
        "al_se_err_rise_stopped": "Redoxwert erhöht sich nicht wie erwartet ! Salz-Elektrolyse gestoppt !",
        "al_se_err_rise": "Redoxwert erhöht sich nicht wie erwartet",
        "al_ph_dosing_stopped": "pH-Wert reagiert nicht wie erwartet ! pH-Dosierung gestoppt !",
        "al_mv_dosing_stopped": "Redox-Wert reagiert nicht wie erwartet ! Chlor-Dosierung gestoppt !",
        "al_ph_minus_empty": "pH-Minus Kanister leer",
        "al_ph_plus_empty": "pH-Plus Kanister leer",
        "al_salt_low_stopped": "Salz-Gehalt zu gering ! Salz-Elektrolyse gestoppt !",
        "al_salt_low_cell_protection": "Salz-Gehalt zu gering !  Zellenschutz-Betrieb (geringe Produktion) !",
        "al_salt_low_pre_warning": "Salzgehalt unter dem bevorzugten Wert",
        "al_se_production_low": "Produktionsleistung der Salz-Elektrolyse zu gering",
        "al_ph_too_high": "pH-Messwert zu hoch",
        "al_ph_too_low": "pH-Messwert zu niedrig",
        "al_se_t_low_stopped": "Wassertemperatur zu gering Salz-Elektrolyse gestoppt",
        "al_se_t_low_stopped_user": "Wassertemperatur gering Salz-Elektrolyse gestoppt",
        "al_se_t_low_cell_protection": "Wassertemperatur zu gering Zellenschutz-Betrieb (geringe Produktion)",
        "al_mv_too_high": "Redox-Messwert zu hoch",
        "al_mv_too_low": "Redox-Messwert zu gering",
        "al_se_no_current": "Kein Zellenstrom",
        "al_filtration_short": "Tägliche Filter-Laufzeit möglicherweise zu kurz",
        "al_cl_empty": "Chlor Kanister leer",
        "enjoy": "Alles in Ordnung. Genießen Sie Ihren Pool!",
        "al_fm_connection_lost": "Verbindung zum Control Module verloren",
        "al_fm_connection_unstable": "Verbindung zum Control Module instabil",
        "al_sw_update_required": "Software Update erforderlich",
        "al_se_fault_one_polarity": "Fehler im Salzelektrolysesystem (0x01R)",
        "al_se_fault_voltage_ok": "Salzelektrolyse: keine Produktion",
        "al_se_fault_voltage_not_ok": "Fehler im Salzelektrolysesystem (0x02V)",
        "al_ph_dos_limit": "Tägliche pH-Dosierungsgrenze erreicht ! pH-Dosierung gestoppt !",
        "al_cl_dos_limit": "Tägliche Chlordosierungsgrenze erreicht! Chlordosierung gestoppt !",
        "al_ph_out_of_range": "pH-Wert außerhalb des Bereichs ! pH-Dosierung und Desinfektion gestoppt !",
        "al_mv_out_of_range": "Redox (mV) Messwert außerhalb des Bereichs ! Chlordosierung gestoppt !",
        "al_se_mv_out_of_range": "Redox (mV) Messwert außerhalb des Bereichs ! Salz-Elektrolyse gestoppt !",
    },
    "fr": {
        "al_no_flow_bnc": "Pompe de filtration arrêtée (pas de débit)",
        "al_no_flow_230V": "Pompe de filtration arrêtée (pas de signal 230V~ de la pompe de filtration)",
        "al_start_delay": "Délai de démarrage",
        "al_se_gas_detected": "Gaz détecté dans la cellule ! Electrolyse de sel arrêtée !",
        "al_se_err_setpoint_safe_mode": "Mesure redox trop basse depuis plusieurs jours ! Electrolyse en mode \"Safe\" !",
        "al_se_err_setpoint_stopped": "Mesure redox trop basse depuis plusieurs jours ! Electrolyse arrêtée !",
        "al_se_err_setpoint": "Mesure redox trop basse depuis plusieurs jours",
        "al_se_err_rise_safe_mode": "La mesure redox n'augmente pas comme prévu ! Electrolyse en mode \"Safe\" !",
        "al_se_err_rise_stopped": "La mesure redox n'augmente pas comme prévu ! Electrolyse arrêtée !",
        "al_se_err_rise": "La mesure redox n'augmente pas comme prévu",
        "al_ph_dosing_stopped": "La mesure pH ne réagit pas comme prévu ! Dosage pH arrêté !",
        "al_mv_dosing_stopped": "La mesure redox ne réagit pas comme prévu ! Dosage chlore arrêté !",
        "al_ph_minus_empty": "Bidon de pH-Minus vide",
        "al_ph_plus_empty": "Bidon de pH-Plus vide",
        "al_salt_low_stopped": "Taux de sel trop bas ! Electrolyse arrêtée !",
        "al_salt_low_cell_protection": "Taux de sel trop faible ! Production réduite (protection cellule)  !",
        "al_salt_low_pre_warning": "Taux de sel inférieur au taux préféré",
        "al_se_production_low": "Production par électrolyse trop faible",
        "al_ph_too_high": "Mesure pH trop haute",
        "al_ph_too_low": "Mesure pH trop basse",
        "al_se_t_low_stopped": "Température de l'eau trop basse Electrolyse arrêtée",
        "al_se_t_low_stopped_user": "Température de l'eau basse Electrolyse arrêtée",
        "al_se_t_low_cell_protection": "Température de l'eau trop basse Production réduite (protection cellule)",
        "al_mv_too_high": "Mesure redox trop haute",
        "al_mv_too_low": "Mesure redox trop basse",
        "al_se_no_current": "Pas de courant cellule",
        "al_filtration_short": "Temps de filtration journalier potentiellement trop faible",
        "al_cl_empty": "Bidon de Chloriliquide vide",
        "enjoy": "Tout va bien. Profitez de votre piscine !",
        "al_fm_connection_lost": "Connexion au S&E Control Module perdue",
        "al_fm_connection_unstable": "Connexion au S&E Control Module instable",
        "al_sw_update_required": "Mise à jour logiciel nécessaire",
        "al_se_fault_one_polarity": "Défaut du système d'électrolyse de sel (0x01R)",
        "al_se_fault_voltage_ok": "électrolyse de sel pas de production",
        "al_se_fault_voltage_not_ok": "Défaut du système d'électrolyse de sel (0x02V)",
        "al_ph_dos_limit": "Limite quotidienne de dosage du pH atteinte ! Dosage du pH arrêté !",
        "al_cl_dos_limit": "Limite quotidienne de dosage de chlore atteinte ! Dosage de chlore arrêté !",
        "al_ph_out_of_range": "Mesure du pH hors plage ! Dosage du pH et désinfection arrêtés !",
        "al_mv_out_of_range": "Lecture redox (mV) hors plage ! Dosage de chlore arrêté !",
        "al_se_mv_out_of_range": "Lecture redox (mV) hors plage ! Electrolyse de sel arrêtée !",
    },
    "es": {
        "al_no_flow_bnc": "Bomba de filtración apagada (no hay caudal)",
        "al_no_flow_230V": "Bomba de filtración apagada (no hay señal 230V~ de la bomba del filtro)",
        "al_start_delay": "Retraso de encendido",
        "al_se_gas_detected": "Gas detectado en la célula ¡ La electrólisis salina se ha detenido !",
        "al_se_err_setpoint_safe_mode": "Lectura redox es muy baja después de varios días   ¡ Electrólisis en modo \"Seguro\" !",
        "al_se_err_setpoint_stopped": "Lectura redox es muy baja después de varios días   ¡ La electrólisis salina se detuvo !",
        "al_se_err_setpoint": "La lectura de redox es muy baja después de varios días.",
        "al_se_err_rise_safe_mode": "Lectura redox no sube como se espera. ¡ Electrólisis funciona en modo \"Seguro\" !",
        "al_se_err_rise_stopped": "Lectura redox no sube como se espera. ¡ La electrólisis salina se detuvo !",
        "al_se_err_rise": "La lectura de redox no sube como se espera",
        "al_ph_dosing_stopped": "Lectura pH no reacciona como se espera ¡ Dosificación de pH detenida !",
        "al_mv_dosing_stopped": "La lectura redox no reacciona como se espera ¡ Dosificación de cloro detenida !",
        "al_ph_minus_empty": "Envase de pH-Minus vacío",
        "al_ph_plus_empty": "Envase de pH-Plus vacío",
        "al_salt_low_stopped": "La tasa de sal es demasiado baja ¡ La electrólisis salina se ha detenido !",
        "al_salt_low_cell_protection": "La tasa de sal es demasiado baja ¡ Protección de la célula (baja producción) !",
        "al_salt_low_pre_warning": "Nivel de sal por debajo del nivel preferido",
        "al_se_production_low": "La producción por electrólisis es muy baja",
        "al_ph_too_high": "La lectura del pH es demasiado alta",
        "al_ph_too_low": "La lectura del pH es demasiado baja",
        "al_se_t_low_stopped": "La temperatura del agua es demasiado baja La electrólisis salina se ha detenido",
        "al_se_t_low_stopped_user": "La temperatura del agua es baja La electrólisis salina se ha detenido",
        "al_se_t_low_cell_protection": "La temperatura del agua es demasiado baja Protección de la célula (baja producción)",
        "al_mv_too_high": "La lectura de redox es demasiado alta",
        "al_mv_too_low": "La lectura de redox es demasiado baja",
        "al_se_no_current": "No hay corriente en la célula",
        "al_filtration_short": "El tiempo de filtración diario es muy corto",
        "al_cl_empty": "Envase de cloro vacío",
        "enjoy": "Todo está bien. Disfrute de su piscina!",
        "al_fm_connection_lost": "Conexión perdida con módulo Smart&Easy",
        "al_fm_connection_unstable": "Conexión inestable con módulo Smart&Easy",
        "al_sw_update_required": "Se requiere actualización del software",
        "al_se_fault_one_polarity": "Fallo del sistema de electrólisis de sal (0x01R)",
        "al_se_fault_voltage_ok": "Electrólisis de sal sin producción",
        "al_se_fault_voltage_not_ok": "Fallo del sistema de electrólisis de sal (0x02V)",
        "al_ph_dos_limit": "Límite de dosificación diario de pH superado ¡ Se ha detenido la dosificación de pH !",
        "al_cl_dos_limit": "Límite de dosificación diario de cloro superado ¡ Se ha detenido la dosificación de cloro !",
        "al_ph_out_of_range": "¡Lectura de pH fuera de rango! ¡Dosificación de pH y desinfección detenidas!",
        "al_mv_out_of_range": "¡Lectura de redox (mV) fuera de rango! ¡Dosificación de cloro detenida!",
        "al_se_mv_out_of_range": "¡Lectura de redox (mV) fuera de rango! ¡ La electrólisis salina se ha detenido !",
    },
    "it": {
        "al_no_flow_bnc": "Pompa di filtrazione spenta (nessun segnale dal flussostato a paletta)",
        "al_no_flow_230V": "Pompa di filtrazione spenta (nessun segnale 230V~ dalla pompa di filtrazione)",
        "al_start_delay": "Ritardo avviamento",
        "al_se_gas_detected": "Rilevazione gas nella cella ! Stop elettrolisi !",
        "al_se_err_setpoint_safe_mode": "Lettura redox troppo bassa per diversi giorni ! Esecuzione elettrolisi in modalità provvisoria !",
        "al_se_err_setpoint_stopped": "Lettura redox troppo bassa per diversi giorni ! Stop elettrolisi !",
        "al_se_err_setpoint": "Lettura redox troppo bassa per diversi giorni",
        "al_se_err_rise_safe_mode": "La lettura redox non aumenta come previsto ! Esecuzione elettrolisi in modalità provvisoria !",
        "al_se_err_rise_stopped": "La lettura redox non aumenta come previsto ! Stop elettrolisi !",
        "al_se_err_rise": "La lettura redox non aumenta come previsto",
        "al_ph_dosing_stopped": "La lettura pH non reagisce come previsto ! Stop dosaggio pH !",
        "al_mv_dosing_stopped": "La lettura redox non reagisce come previsto ! Stop dosaggio cloro !",
        "al_ph_minus_empty": "Tanica pH-Minus vuota",
        "al_ph_plus_empty": "Tanica pH+Plus vuota",
        "al_salt_low_stopped": "Livello sale troppo basso ! Stop elettrolisi !",
        "al_salt_low_cell_protection": "Livello sale troppo basso ! Modalità protezione cella (bassa produzione) !",
        "al_salt_low_pre_warning": "Quantità sale al di sotto del livello desiderato",
        "al_se_production_low": "Produzione elettrolisi troppo bassa",
        "al_ph_too_high": "Lettura pH troppo alta",
        "al_ph_too_low": "Lettura pH troppo bassa",
        "al_se_t_low_stopped": "Temperatura dell'acqua troppo bassa ! Stop elettrolisi !",
        "al_se_t_low_stopped_user": "Temperatura dell'acqua troppo bassa ! Stop elettrolisi !",
        "al_se_t_low_cell_protection": "Temperatura dell'acqua troppo bassa ! Modalità protezione cella (bassa produzione) !",
        "al_mv_too_high": "Lettura redox troppo alta",
        "al_mv_too_low": "Lettura redox troppo bassa",
        "al_se_no_current": "Nessuna corrente sulla cella",
        "al_filtration_short": "Tempo di filtrazione giornaliero troppo breve",
        "al_cl_empty": "Tanica cloro vuota",
        "enjoy": "Tutto OK. Goditi la tua piscina!",
        "ev_sw_reset": "Reset Software",
        "ev_system_start": "Accensione",
        "ev_default_reset": "Reset Default",
        "al_fm_connection_lost": "Connessione persa con S&E Control Module",
        "al_fm_connection_unstable": "Connessione instabile con S&E Control Module",
        "al_sw_update_required": "È richiesto l'aggiornamento del software",
        "al_se_fault_one_polarity": "Guasto al sistema di elettrolisi del sale (0x01R)",
        "al_se_fault_voltage_ok": "Elettrolisi del sale - nessuna produzione",
        "al_se_fault_voltage_not_ok": "Guasto al sistema di elettrolisi del sale (0x02V)",
        "al_ph_dos_limit": "Limite giornaliero di dosaggio del pH raggiunto ! Dosaggio del pH interrotto !",
        "al_cl_dos_limit": "Limite giornaliero di dosaggio cloro raggiunto ! Dosaggio del cloro interrotto !",
        "al_ph_out_of_range": "Valore pH fuori range ! Dosaggio pH e disinfezione interrotti !",
        "al_mv_out_of_range": "Lettura redox (mV) fuori range ! Dosaggio cloro interrotto !",
        "al_se_mv_out_of_range": "Lettura redox (mV) fuori range ! Stop elettrolisi !",
    },
    "pl": {
        "al_no_flow_bnc": "Pompa obiegowa wył. (brak sygnału przepływu)",
        "al_no_flow_230V": "Pompa obiegowa wyłączona  (brak sygnału 230V~)",
        "al_start_delay": "Opóźnienie startu",
        "al_se_gas_detected": "Wykryto gaz w celi ! Zatrzymano elektrolizę soli !",
        "al_se_err_setpoint_safe_mode": "Odczyt Rx zbyt niski! Praca w trybie awaryjnym!",
        "al_se_err_setpoint_stopped": "Odczyt Rx zbyt niski! Zatrzymano elektrolizę soli!",
        "al_se_err_setpoint": "Odczyt redoks zbyt niski przez kilka dni",
        "al_se_err_rise_safe_mode": "Odczyt Rx nie wzrasta wg ustawień! Tryb awaryjny!",
        "al_se_err_rise_stopped": "Odczyt Rx nie rośnie wg ustaw.! Praca zatrzymana!",
        "al_se_err_rise": "Odczyt Rx nie rośnie zgodnie z ustawieniami",
        "al_ph_dosing_stopped": "Odczyt pH nie reaguje wg ustawień ! Dozowanie pH zatrzymane!",
        "al_mv_dosing_stopped": "Odczyt Rx nie reaguje wg ustawień ! Zatrzymano dozowanie chloru !",
        "al_ph_minus_empty": "Zbiornik pH-Minus pusty",
        "al_ph_plus_empty": "Zbiornik pH-Plus pusty",
        "al_salt_low_stopped": "Zasolenie zbyt niskie ! Zatrzymano elektrolizę soli !",
        "al_salt_low_cell_protection": "Zasolenie zbyt niskie ! Tryb ochrony celi (niska produkcja) !",
        "al_salt_low_pre_warning": "Zasolenie poniżej preferowanego poziomu",
        "al_se_production_low": "Zbyt niska produkcja soli",
        "al_ph_too_high": "Odczyt pH zbyt wysoki",
        "al_ph_too_low": "Odczyt pH zbyt niski",
        "al_se_t_low_stopped": "Zbyt niska temperatura wody  Elektroliza soli zatrzymana",
        "al_se_t_low_stopped_user": "Niska temperatura wody  Elektroliza soli zatrzymana",
        "al_se_t_low_cell_protection": "Zbyt niska temperatura wody  Tryb ochrony celi (niska produkcja)",
        "al_mv_too_high": "Odczyt redoks zbyt wysoki",
        "al_mv_too_low": "Odczyt redoks zbyt niski",
        "al_se_no_current": "Brak napięcia w celi",
        "al_filtration_short": "Potencjalnie zbyt krótki dzienny czas filtracji",
        "al_cl_empty": "Zbiornik z chlorem pusty",
        "enjoy": "Wszystko jest w porządku. Ciesz się swoim basenem!",
        "ev_sw_reset": "Reset oprogramowania",
        "ev_system_start": "Zasilanie włączone",
        "ev_default_reset": "Kasowanie stanów domyślnych",
        "al_fm_connection_lost": "Moduł sterujący: utracono połączenie",
        "al_fm_connection_unstable": "Moduł sterujący: połączenie niestabilne",
        "al_sw_update_required": "Wymagana aktualizacja oprogramowania",
        "al_se_fault_one_polarity": "Błąd systemu elektrolizy soli (0x01R)",
        "al_se_fault_voltage_ok": "Elektroliza soli bez produkcji",
        "al_se_fault_voltage_not_ok": "Błąd systemu elektrolizy soli (0x02V)",
        "al_ph_dos_limit": "Osiągnięto dzienny limit dozowania pH ! Dozowanie pH zatrzymane !",
        "al_cl_dos_limit": "Osiągnięto dzienny limit dozowania chloru ! Dozowanie chloru zatrzymane !",
        "al_ph_out_of_range": "Odczyt pH poza zakresem ! Dozowanie pH i dezynfekcja zatrzymane !",
        "al_mv_out_of_range": "Odczyt Redox (mV) poza zakresem ! Dozowanie chloru zatrzymane !",
        "al_se_mv_out_of_range": "Odczyt Redox (mV) poza zakresem ! Zatrzymano elektrolizę soli !",
    },
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

        previous_keys = {message["key"] for message in self._messages}
        self._message_codes = [self._normalize_message_code(code) for code in raw_codes]
        self._messages = [self._message_details(code) for code in self._message_codes]

        # Fire a bus event for every newly appearing message. On the first
        # payload after startup all active messages are announced once.
        if self.hass is not None:
            for message in self._messages:
                if message["key"] in previous_keys:
                    continue
                self.hass.bus.async_fire(
                    BAYROL_MESSAGE_EVENT,
                    {
                        "entry_id": self._config_entry.entry_id,
                        "device_id": self._config_entry.data[BAYROL_DEVICE_ID],
                        **message,
                    },
                )

        keys = [message["key"] for message in self._messages]
        state = ", ".join(message["message"] for message in self._messages) or "none"
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
