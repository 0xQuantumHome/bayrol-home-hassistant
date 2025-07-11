"""Constants for the Bayrol integration."""

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorStateClass,
)

DOMAIN = "bayrol"

BAYROL_ACCESS_TOKEN = "bayrol_access_token"
BAYROL_DEVICE_ID = "bayrol_device_id"
BAYROL_DEVICE_TYPE = "bayrol_device_type"
BAYROL_APP_LINK_CODE = "bayrol_app_link_code"

BAYROL_HOST = "www.bayrol-poolaccess.de"
BAYROL_PORT = 8083

# MQTT value mappings for AS5 device
VALUE_TO_MQTT_AUTOMATIC = {
    "0.25x": "19.3",
    "0.5x": "19.4",
    "0.75x": "19.5",
    "1.0x": "19.6",
    "1.25x": "19.7",
    "1.5x": "19.8",
    "2x": "19.9",
    "3x": "19.10",
    "5x": "19.11",
    "10x": "19.12",
    "On": "19.17",
    "Off": "19.18",
    "Constant production": "19.106",
    "Auto Plus": "19.115",
    "Auto": "19.195",
    "Full": "19.258",
    "Empty": "19.259",
}

# Reverse mapping for MQTT values to display values
MQTT_TO_VALUE_AUTOMATIC = {v: k for k, v in VALUE_TO_MQTT_AUTOMATIC.items()}

VALUE_TO_MQTT_PM5 = {
    "On": "7408",
    "Off": "7407",
    "Auto": "7427",
}

# Reverse mapping for MQTT values to display values
MQTT_TO_VALUE_PM5 = {v: k for k, v in VALUE_TO_MQTT_PM5.items()}

# Common sensor types for Automatic devices
SENSOR_TYPES_AUTOMATIC = {
    "4.2": {
        "name": "pH Target",
        "device_class": SensorDeviceClass.PH,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 10,
        "unit_of_measurement": None,
        "entity_type": "select",
        "options": [
            6.2,
            6.3,
            6.4,
            6.5,
            6.6,
            6.7,
            6.8,
            6.9,
            7.0,
            7.1,
            7.2,
            7.3,
            7.4,
            7.5,
            7.6,
            7.7,
            7.8,
            7.9,
            8.0,
            8.1,
            8.2,
        ],
    },
    "4.3": {
        "name": "pH Alert Max",
        "device_class": SensorDeviceClass.PH,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 10,
        "unit_of_measurement": None,
        "entity_type": "select",
        "options": [
            7.2,
            7.3,
            7.4,
            7.5,
            7.6,
            7.7,
            7.8,
            7.9,
            8.0,
            8.1,
            8.2,
            8.3,
            8.4,
            8.5,
            8.6,
            8.7,
        ],
    },
    "4.4": {
        "name": "pH Alert Min",
        "device_class": SensorDeviceClass.PH,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 10,
        "unit_of_measurement": None,
        "entity_type": "select",
        "options": [
            5.7,
            5.8,
            5.9,
            6.0,
            6.1,
            6.2,
            6.3,
            6.4,
            6.5,
            6.6,
            6.7,
            6.8,
            6.9,
            7.0,
            7.1,
            7.2,
        ],
    },
    "4.5": {
        "name": "pH Dosing Control Time Interval",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 1,
        "unit_of_measurement": "min",
        "entity_type": "sensor",
    },
    "4.7": {
        "name": "Minutes Counter / Reset every hour",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 1,
        "unit_of_measurement": "min",
        "entity_type": "sensor",
    },
    "4.26": {
        "name": "Redox Alert Max",
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 1,
        "unit_of_measurement": "mV",
        "entity_type": "select",
        "options": [
            995,
            990,
            985,
            980,
            975,
            970,
            965,
            960,
            955,
            950,
            945,
            940,
            935,
            930,
            925,
            920,
            915,
            910,
            905,
            900,
            895,
            890,
            885,
            880,
            875,
            870,
            865,
            860,
            855,
            850,
            845,
            840,
            835,
            830,
            825,
            820,
            815,
            810,
            805,
            800,
            795,
            790,
            785,
            780,
            775,
            770,
            765,
            760,
            755,
            750,
            745,
            740,
            735,
            730,
            725,
            720,
            715,
            710,
            705,
            700,
            695,
            690,
            685,
            680,
            675,
            670,
            665,
            660,
            655,
            650,
            645,
            640,
            635,
            630,
            625,
            620,
            615,
            610,
            605,
            600,
            595,
            590,
            585,
            580,
            575,
            570,
            565,
            560,
            555,
            550,
            545,
            540,
            535,
            530,
            525,
            520,
            515,
            510,
            505,
            500,
        ],
    },
    "4.27": {
        "name": "Redox Alert Min",
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 1,
        "unit_of_measurement": "mV",
        "entity_type": "select",
        "options": [
            850,
            845,
            840,
            835,
            830,
            825,
            820,
            815,
            810,
            805,
            800,
            795,
            790,
            785,
            780,
            775,
            770,
            765,
            760,
            755,
            750,
            745,
            740,
            735,
            730,
            725,
            720,
            715,
            710,
            705,
            700,
            695,
            690,
            685,
            680,
            675,
            670,
            665,
            660,
            655,
            650,
            645,
            640,
            635,
            630,
            625,
            620,
            615,
            610,
            605,
            600,
            595,
            590,
            585,
            580,
            575,
            570,
            565,
            560,
            555,
            550,
            545,
            540,
            535,
            530,
            525,
            520,
            515,
            510,
            505,
            500,
            495,
            490,
            485,
            480,
            475,
            470,
            465,
            460,
            455,
            450,
            445,
            440,
            435,
            430,
            425,
            420,
            415,
            410,
            405,
            400,
            395,
            390,
            385,
            380,
            375,
            370,
            365,
            360,
            355,
            350,
            345,
            340,
            335,
            330,
            325,
            320,
            315,
            310,
            305,
            300,
            295,
            290,
            285,
            280,
            275,
            270,
            265,
            260,
            255,
            250,
            245,
            240,
            235,
            230,
            225,
            220,
            215,
            210,
            205,
            200,
        ],
    },
    "4.28": {
        "name": "Redox Target",
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 1,
        "unit_of_measurement": "mV",
        "entity_type": "select",
        "options": [
            950,
            945,
            940,
            935,
            930,
            925,
            920,
            915,
            910,
            905,
            900,
            895,
            890,
            885,
            880,
            875,
            870,
            865,
            860,
            855,
            850,
            845,
            840,
            835,
            830,
            825,
            820,
            815,
            810,
            805,
            800,
            795,
            790,
            785,
            780,
            775,
            770,
            765,
            760,
            755,
            750,
            745,
            740,
            735,
            730,
            725,
            720,
            715,
            710,
            705,
            700,
            695,
            690,
            685,
            680,
            675,
            670,
            665,
            660,
            655,
            650,
            645,
            640,
            635,
            630,
            625,
            620,
            615,
            610,
            605,
            600,
            595,
            590,
            585,
            580,
            575,
            570,
            565,
            560,
            555,
            550,
            545,
            540,
            535,
            530,
            525,
            520,
            515,
            510,
            505,
            500,
            495,
            490,
            485,
            480,
            475,
            470,
            465,
            460,
            455,
            450,
            445,
            440,
            435,
            430,
            425,
            420,
            415,
            410,
            405,
            400,
        ],
    },
    "4.34": {
        "name": "Minimal Approach to Control the pH",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 100,
        "unit_of_measurement": None,
        "entity_type": "sensor",
    },
    "4.37": {
        "name": "Start Delay",
        "device_class": None,
        "state_class": None,
        "coefficient": 1,
        "unit_of_measurement": "min",
        "entity_type": "select",
        "options": [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            21,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            30,
            31,
            32,
            33,
            34,
            35,
            36,
            37,
            38,
            39,
            40,
            41,
            42,
            43,
            44,
            45,
            46,
            47,
            48,
            49,
            50,
            51,
            52,
            53,
            54,
            55,
            56,
            57,
            58,
            59,
            60,
        ],
    },
    "4.38": {
        "name": "pH Dosing Cycle",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 1,
        "unit_of_measurement": "s",
        "entity_type": "sensor",
    },
    "4.47": {
        "name": "pH Dosing Speed",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 1,
        "unit_of_measurement": "%",
        "entity_type": "sensor",
    },
    "4.67": {
        "name": "SW Version",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 100,
        "unit_of_measurement": None,
        "entity_type": "sensor",
    },
    "4.68": {
        "name": "SW Date",
        "device_class": None,
        "state_class": None,
        "coefficient": -1,  # Treat result as string
        "unit_of_measurement": None,
        "entity_type": "sensor",
    },
    "4.69": {
        "name": "Hourly Counter / Reset every 24h",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 1,
        "unit_of_measurement": "h",
        "entity_type": "sensor",
    },
    "4.82": {
        "name": "Redox",
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 1,
        "unit_of_measurement": "mV",
        "entity_type": "sensor",
    },
    "4.89": {
        "name": "pH Dosing Rate",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 1,
        "unit_of_measurement": "%",
        "entity_type": "sensor",
    },
    "4.98": {
        "name": "Temperature",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 10,
        "unit_of_measurement": "°C",
        "entity_type": "sensor",
    },
    "4.102": {
        "name": "Conductivity",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 10,
        "unit_of_measurement": "mS/cm",
        "entity_type": "sensor",
    },
    "4.107": {
        "name": "Battery Voltage",
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 100,
        "unit_of_measurement": "V",
        "entity_type": "sensor",
    },
    "4.182": {
        "name": "pH",
        "device_class": SensorDeviceClass.PH,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 10,
        "unit_of_measurement": None,
        "entity_type": "sensor",
    },
    "5.3": {
        "name": "pH Production Rate",
        "device_class": None,
        "state_class": None,
        "coefficient": None,
        "unit_of_measurement": None,
        "entity_type": "select",
        "options": [
            "0.25x",
            "0.5x",
            "0.75x",
            "1.0x",
            "1.25x",
            "1.5x",
            "2x",
            "3x",
            "5x",
            "10x",
        ],
    },
    "5.80": {
        "name": "pH Minus Canister Status",
        "device_class": None,
        "state_class": None,
        "coefficient": None,
        "unit_of_measurement": None,
        "entity_type": "sensor",
    },
    "5.98": {
        "name": "Filtration",
        "device_class": None,
        "state_class": None,
        "coefficient": None,
        "unit_of_measurement": None,
        "entity_type": "sensor",
    },
}

# Additional sensor types for Automatic SALT
SENSOR_TYPES_AUTOMATIC_SALT = {
    **SENSOR_TYPES_AUTOMATIC,  # Include all base sensors
    "4.51": {
        "name": "Polarity Reversal Times",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 1,
        "unit_of_measurement": "min",
        "entity_type": "sensor",
    },
    "4.66": {
        "name": "Minimum Redox Produktion",
        "device_class": None,
        "state_class": None,
        "coefficient": 1,
        "unit_of_measurement": "%",
        "entity_type": "select",
        "options": [
            100,
            95,
            90,
            85,
            80,
            75,
            70,
            65,
            60,
            55,
            50,
            45,
            40,
            35,
            30,
            25,
            20,
            15,
        ],
    },
    "4.91": {
        "name": "Electrolyzer Production Rate",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 1,
        "unit_of_measurement": "%",
        "entity_type": "sensor",
    },
    "4.100": {
        "name": "Salt",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 10,
        "unit_of_measurement": "g/l",
        "entity_type": "sensor",
    },
    "4.104": {
        "name": "Electrolyzer Voltage",
        "device_class": SensorDeviceClass.VOLTAGE,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 10,
        "unit_of_measurement": "V",
        "entity_type": "sensor",
    },
    "4.105": {
        "name": "Electrolyzer Current",
        "device_class": SensorDeviceClass.CURRENT,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 10,
        "unit_of_measurement": "A",
        "entity_type": "sensor",
    },
    "4.112": {
        "name": "Time Before Next Polarity Reversal",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 1,
        "unit_of_measurement": "s",
        "entity_type": "sensor",
    },
    "4.119": {
        "name": "Time Since Polarity Reversal",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 1,
        "unit_of_measurement": "s",
        "entity_type": "sensor",
    },
    "4.144": {
        "name": "Salt Preferred Level",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 10,
        "unit_of_measurement": "g/l",
        "entity_type": "select",
        "options": [
            1.0,
            1.1,
            1.2,
            1.3,
            1.4,
            1.5,
            1.6,
            1.7,
            1.8,
            1.9,
            2.0,
            2.1,
            2.2,
            2.3,
            2.4,
            2.5,
            2.6,
            2.7,
            2.8,
            2.9,
            3.0,
            3.1,
            3.2,
            3.3,
            3.4,
            3.5,
            3.6,
            3.7,
            3.8,
            3.9,
            4.0,
            4.1,
            4.2,
            4.3,
            4.4,
            4.5,
            4.6,
            4.7,
            4.8,
            4.9,
            5.0,
        ],
    },
    "5.40": {
        "name": "Redox ON / OFF",
        "device_class": None,
        "state_class": None,
        "coefficient": None,
        "unit_of_measurement": None,
        "entity_type": "select",
        "options": [
            "On",
            "Off",
        ],
    },
    "5.41": {
        "name": "Redox Mode",
        "device_class": None,
        "state_class": None,
        "coefficient": None,
        "unit_of_measurement": None,
        "entity_type": "select",
        "options": [
            "Auto",
            "Auto Plus",
            "Constant production",
        ],
    },
}

# Additional sensor types for Automatic Cl-pH
SENSOR_TYPES_AUTOMATIC_CL_PH = {
    **SENSOR_TYPES_AUTOMATIC,  # Include all base sensors
    "4.90": {
        "name": "Cl Dosing Rate",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 1,
        "unit_of_measurement": "%",
        "entity_type": "sensor",
    },
    "5.175": {
        "name": "Cl Adjust Dosing Amount",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 1,
        "unit_of_measurement": "%",
        "entity_type": "select",
        "options": [
            "0.25x",
            "0.5x",
            "0.75x",
            "1.0x",
            "1.25x",
            "1.5x",
            "2x",
            "3x",
            "5x",
            "10x",
        ],
    },
    "5.169": {
        "name": "Cl Canister Status",
        "device_class": None,
        "state_class": None,
        "coefficient": None,
        "unit_of_measurement": None,
        "entity_type": "sensor",
    },
}

# Sensor types for PM5 Chlorine
SENSOR_TYPES_PM5_CHLORINE = {
    "4.3001": {
        "name": "pH Target",
        "device_class": SensorDeviceClass.PH,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 100,
        "unit_of_measurement": None,
        "entity_type": "select",
        "options": [
            6.2,
            6.3,
            6.4,
            6.5,
            6.6,
            6.7,
            6.8,
            6.9,
            7.0,
            7.1,
            7.2,
            7.3,
            7.4,
            7.5,
            7.6,
            7.7,
            7.8,
            7.9,
            8.0,
            8.1,
            8.2,
        ],
    },
    "4.3002": {
        "name": "pH Alert Min",
        "device_class": SensorDeviceClass.PH,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 100,
        "unit_of_measurement": None,
        "entity_type": "select",
        "options": [
            5.7,
            5.8,
            5.9,
            6.0,
            6.1,
            6.2,
            6.3,
            6.4,
            6.5,
            6.6,
            6.7,
            6.8,
            6.9,
            7.0,
            7.1,
            7.2,
        ],
    },
    "4.3003": {
        "name": "pH Alert Max",
        "device_class": SensorDeviceClass.PH,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 100,
        "unit_of_measurement": None,
        "entity_type": "select",
        "options": [
            7.2,
            7.3,
            7.4,
            7.5,
            7.6,
            7.7,
            7.8,
            7.9,
            8.0,
            8.1,
            8.2,
            8.3,
            8.4,
            8.5,
            8.6,
            8.7,
        ],
    },
    "4.3049": {
        "name": "Redox Target",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 1,
        "unit_of_measurement": "mV",
        "entity_type": "select",
        "options": [
            950,
            945,
            940,
            935,
            930,
            925,
            920,
            915,
            910,
            905,
            900,
            895,
            890,
            885,
            880,
            875,
            870,
            865,
            860,
            855,
            850,
            845,
            840,
            835,
            830,
            825,
            820,
            815,
            810,
            805,
            800,
            795,
            790,
            785,
            780,
            775,
            770,
            765,
            760,
            755,
            750,
            745,
            740,
            735,
            730,
            725,
            720,
            715,
            710,
            705,
            700,
            695,
            690,
            685,
            680,
            675,
            670,
            665,
            660,
            655,
            650,
            645,
            640,
            635,
            630,
            625,
            620,
            615,
            610,
            605,
            600,
            595,
            590,
            585,
            580,
            575,
            570,
            565,
            560,
            555,
            550,
            545,
            540,
            535,
            530,
            525,
            520,
            515,
            510,
            505,
            500,
            495,
            490,
            485,
            480,
            475,
            470,
            465,
            460,
            455,
            450,
            445,
            440,
            435,
            430,
            425,
            420,
            415,
            410,
            405,
            400,
        ],
    },
    "4.3051": {
        "name": "Redox Alert Min",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 1,
        "unit_of_measurement": "mV",
        "entity_type": "select",
        "options": [
            850,
            845,
            840,
            835,
            830,
            825,
            820,
            815,
            810,
            805,
            800,
            795,
            790,
            785,
            780,
            775,
            770,
            765,
            760,
            755,
            750,
            745,
            740,
            735,
            730,
            725,
            720,
            715,
            710,
            705,
            700,
            695,
            690,
            685,
            680,
            675,
            670,
            665,
            660,
            655,
            650,
            645,
            640,
            635,
            630,
            625,
            620,
            615,
            610,
            605,
            600,
            595,
            590,
            585,
            580,
            575,
            570,
            565,
            560,
            555,
            550,
            545,
            540,
            535,
            530,
            525,
            520,
            515,
            510,
            505,
            500,
            495,
            490,
            485,
            480,
            475,
            470,
            465,
            460,
            455,
            450,
            445,
            440,
            435,
            430,
            425,
            420,
            415,
            410,
            405,
            400,
            395,
            390,
            385,
            380,
            375,
            370,
            365,
            360,
            355,
            350,
            345,
            340,
            335,
            330,
            325,
            320,
            315,
            310,
            305,
            300,
            295,
            290,
            285,
            280,
            275,
            270,
            265,
            260,
            255,
            250,
            245,
            240,
            235,
            230,
            225,
            220,
            215,
            210,
            205,
            200,
        ],
    },
    "4.3053": {
        "name": "Redox Alert Max",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 1,
        "unit_of_measurement": "mV",
        "entity_type": "select",
        "options": [
            995,
            990,
            985,
            980,
            975,
            970,
            965,
            960,
            955,
            950,
            945,
            940,
            935,
            930,
            925,
            920,
            915,
            910,
            905,
            900,
            895,
            890,
            885,
            880,
            875,
            870,
            865,
            860,
            855,
            850,
            845,
            840,
            835,
            830,
            825,
            820,
            815,
            810,
            805,
            800,
            795,
            790,
            785,
            780,
            775,
            770,
            765,
            760,
            755,
            750,
            745,
            740,
            735,
            730,
            725,
            720,
            715,
            710,
            705,
            700,
            695,
            690,
            685,
            680,
            675,
            670,
            665,
            660,
            655,
            650,
            645,
            640,
            635,
            630,
            625,
            620,
            615,
            610,
            605,
            600,
            595,
            590,
            585,
            580,
            575,
            570,
            565,
            560,
            555,
            550,
            545,
            540,
            535,
            530,
            525,
            520,
            515,
            510,
            505,
            500,
        ],
    },
    "4.4001": {
        "name": "pH",
        "device_class": SensorDeviceClass.PH,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 100,
        "unit_of_measurement": None,
        "entity_type": "sensor",
    },
    "4.4022": {
        "name": "Redox",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 1,
        "unit_of_measurement": "mV",
        "entity_type": "sensor",
    },
    "4.4033": {
        "name": "Water Temperature",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 10,
        "unit_of_measurement": "°C",
        "entity_type": "sensor",
    },
    "4.4069": {
        "name": "Air Temperature",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 10,
        "unit_of_measurement": "°C",
        "entity_type": "sensor",
    },
    "4.4132": {
        "name": "Active Alarms",
        "device_class": None,
        "state_class": SensorStateClass.MEASUREMENT,
        "coefficient": 1,
        "unit_of_measurement": None,
        "entity_type": "sensor",
    },
    "5.5433": {
        "name": "Out 1",
        "device_class": None,
        "state_class": None,
        "coefficient": None,
        "unit_of_measurement": None,
        "entity_type": "select",
        "options": [
            "On",
            "Off",
            "Auto",
        ],
    },
    "5.5434": {
        "name": "Out 2",
        "device_class": None,
        "state_class": None,
        "coefficient": None,
        "unit_of_measurement": None,
        "entity_type": "select",
        "options": [
            "On",
            "Off",
            "Auto",
        ],
    },
    "5.5435": {
        "name": "Out 3",
        "device_class": None,
        "state_class": None,
        "coefficient": None,
        "unit_of_measurement": None,
        "entity_type": "select",
        "options": [
            "On",
            "Off",
            "Auto",
        ],
    },
    "5.5436": {
        "name": "Out 4",
        "device_class": None,
        "state_class": None,
        "coefficient": None,
        "unit_of_measurement": None,
        "entity_type": "select",
        "options": [
            "On",
            "Off",
            "Auto",
        ],
    },
    "5.6012": {
        "name": "pH Pump",
        "device_class": None,
        "state_class": None,
        "coefficient": None,
        "unit_of_measurement": None,
        "entity_type": "sensor",
    },
    "5.6015": {
        "name": "Redox Pump Status",
        "device_class": None,
        "state_class": None,
        "coefficient": None,
        "unit_of_measurement": None,
        "entity_type": "sensor",
    },
    "5.6064": {
        "name": "pH Canister Level",
        "device_class": None,
        "state_class": None,
        "coefficient": None,
        "unit_of_measurement": None,
        "entity_type": "sensor",
    },
    "5.6065": {
        "name": "pH Status",
        "device_class": None,
        "state_class": None,
        "coefficient": None,
        "unit_of_measurement": None,
        "entity_type": "sensor",
    },
    "5.6068": {
        "name": "Redox Canister Level",
        "device_class": None,
        "state_class": None,
        "coefficient": None,
        "unit_of_measurement": None,
        "entity_type": "sensor",
    },
    "5.6069": {
        "name": "Redox Status",
        "device_class": None,
        "state_class": None,
        "coefficient": None,
        "unit_of_measurement": None,
        "entity_type": "sensor",
    },
}
