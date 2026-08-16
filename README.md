[![Static Badge](https://img.shields.io/badge/HACS-Custom-41BDF5?style=for-the-badge&logo=homeassistantcommunitystore&logoColor=white)](https://github.com/hacs/integration) 
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/0xQuantumHome/bayrol-home-hassistant?style=for-the-badge) 
![GitHub Release Date](https://img.shields.io/github/release-date/0xQuantumHome/bayrol-home-hassistant?style=for-the-badge&label=Latest%20Release) [![GitHub Release](https://img.shields.io/github/v/release/0xQuantumHome/bayrol-home-hassistant?style=for-the-badge)](https://github.com/0xQuantumHome/bayrol-home-hassistant/releases)


# Bayrol Pool Access Integration for Home Assistant

This custom integration allows you to monitor your Bayrol Pool Access device in Home Assistant. It uses a direct MQTT connection to the Bayrol Cloud.

## Features

- 35 to 60+ entities per device, depending on the model (pH, Redox, Salt, chlorine, temperatures, alarm thresholds, pump and output states)
- Writable settings as select entities (discrete modes), number entities (targets, alarm limits, delays and temperature setpoints), and switch entities (pH dosing and salt electrolysis)
- Current device messages, including pH, redox, salt, flow and cell warnings
- Real-time updates via MQTT connection

## Tested Devices

- Bayrol Automatic Salt 5 (AS5)
- Bayrol Automatic Cl-pH
- Pool Manager 5 Chlorine

## Supported Entities

The entities you get depend on the device type you select when adding the integration.
The **MQTT ID** is the topic suffix the device publishes under (see [MQTT Debug](#mqtt-debug)), the **Type** is the Home Assistant platform the entity is created on:

- `sensor` – read only
- `select` – writable, pick one of a fixed list of values
- `number` – writable numeric value
- `switch` – writable on/off setting
- `button` – sends a command to the device

### Automatic SALT

| MQTT ID | Name | Type | Unit |
| --- | --- | --- | --- |
| `10` | Messages | sensor | — |
| `4.2` | pH Target | number | — |
| `4.3` | pH Alert Max | number | — |
| `4.4` | pH Alert Min | number | — |
| `4.5` | pH Dosing Control Time Interval | sensor | min |
| `4.7` | Minutes Counter / Reset every hour | sensor | min |
| `4.26` | Redox Alert Max | number | mV |
| `4.27` | Redox Alert Min | number | mV |
| `4.28` | Redox Target | number | mV |
| `4.34` | Minimal Approach to Control the pH | sensor | — |
| `4.37` | Start Delay | number | min |
| `4.38` | pH Dosing Cycle | sensor | s |
| `4.47` | pH Dosing Speed | sensor | % |
| `4.51` | Polarity Reversal Times | sensor | min |
| `4.66` | Minimum Redox Produktion | number | % |
| `4.67` | SW Version | sensor | — |
| `4.68` | SW Date | sensor | — |
| `4.69` | Hourly Counter / Reset every 24h | sensor | h |
| `4.82` | Redox | sensor | mV |
| `4.89` | pH Dosing Rate | sensor | % |
| `4.91` | Electrolyzer Production Rate | sensor | % |
| `4.98` | Temperature | sensor | °C |
| `4.100` | Salt | sensor | g/l |
| `4.102` | Conductivity | sensor | mS/cm |
| `4.104` | Electrolyzer Voltage | sensor | V |
| `4.105` | Electrolyzer Current | sensor | A |
| `4.107` | Battery Voltage | sensor | V |
| `4.112` | Time Before Next Polarity Reversal | sensor | s |
| `4.119` | Time Since Polarity Reversal | sensor | s |
| `4.144` | Salt Preferred Level | number | g/l |
| `4.182` | pH | sensor | — |
| `5.3` | pH Production Rate | select | — |
| `5.29` | Flow Pump Status | sensor | — |
| `5.37` | Gas Sensor | sensor | — |
| `5.40` | Salt electrolysis ON/OFF | switch | — |
| `5.41` | Redox Mode | select | — |
| `5.42` | pH Dosing ON/OFF | switch | — |
| `5.80` | pH Minus Canister Status | sensor | — |
| `5.83` | Cover | sensor | — |
| `5.98` | Flow Contact | sensor | — |
| `5.184` | Filtration mode | select | — |
| `5.186` | Out 1 Mode | select | — |
| `5.187` | Out 2 Mode | select | — |
| `5.188` | Out 3 Mode | select | — |
| `5.189` | Out 4 Mode | select | — |

### Automatic Cl-pH

| MQTT ID | Name | Type | Unit |
| --- | --- | --- | --- |
| `10` | Messages | sensor | — |
| `4.2` | pH Target | number | — |
| `4.3` | pH Alert Max | number | — |
| `4.4` | pH Alert Min | number | — |
| `4.5` | pH Dosing Control Time Interval | sensor | min |
| `4.7` | Minutes Counter / Reset every hour | sensor | min |
| `4.26` | Redox Alert Max | number | mV |
| `4.27` | Redox Alert Min | number | mV |
| `4.28` | Redox Target | number | mV |
| `4.34` | Minimal Approach to Control the pH | sensor | — |
| `4.37` | Start Delay | number | min |
| `4.38` | pH Dosing Cycle | sensor | s |
| `4.47` | pH Dosing Speed | sensor | % |
| `4.67` | SW Version | sensor | — |
| `4.68` | SW Date | sensor | — |
| `4.69` | Hourly Counter / Reset every 24h | sensor | h |
| `4.82` | Redox | sensor | mV |
| `4.89` | pH Dosing Rate | sensor | % |
| `4.90` | Cl Dosing Rate | sensor | % |
| `4.98` | Temperature | sensor | °C |
| `4.102` | Conductivity | sensor | mS/cm |
| `4.107` | Battery Voltage | sensor | V |
| `4.182` | pH | sensor | — |
| `5.3` | pH Production Rate | select | — |
| `5.28` | Flow In Status | sensor | — |
| `5.29` | Flow Pump Status | sensor | — |
| `5.37` | Gas Sensor | sensor | — |
| `5.42` | pH Dosing ON/OFF | switch | — |
| `5.80` | pH Minus Canister Status | sensor | — |
| `5.83` | Cover | sensor | — |
| `5.169` | Cl Canister Status | sensor | — |
| `5.175` | Cl Adjust Dosing Amount | select | % |
| `5.184` | Filtration mode | select | — |
| `5.186` | Out 1 Mode | select | — |
| `5.187` | Out 2 Mode | select | — |
| `5.188` | Out 3 Mode | select | — |
| `5.189` | Out 4 Mode | select | — |

Automatic SALT and Automatic Cl-pH devices also expose MQTT topic `10` as a
`Messages` sensor. Its state contains the stable message keys used by the
previous `bayrol-poolaccess-mqtt` bridge. The `message_codes` attribute keeps
the raw Bayrol codes, `message_keys` exposes the stable keys for automations,
and `data` provides each code, key, severity and readable message. Message text
follows Home Assistant's configured system language (French and English are
supported, with English as the fallback). This includes redox warnings such as
`8.9` to `8.14`, as well as the other current messages shown by PoolAccess.

### PM5 Chlorine

| MQTT ID | Name | Type | Unit |
| --- | --- | --- | --- |
| `4.3001` | pH Target | select | — |
| `4.3002` | pH Alert Min | select | — |
| `4.3003` | pH Alert Max | select | — |
| `4.3017` | Setpoint Chlorine | select | mg/l |
| `4.3018` | Lower Alarm threshold Chlorine | select | mg/l |
| `4.3019` | Upper Alarm threshold Chlorine | select | mg/l |
| `4.3049` | Setpoint Redox | select | mV |
| `4.3051` | Redox Alert Min | select | mV |
| `4.3053` | Redox Alert Max | select | mV |
| `4.3118` | Heating Setpoint | number | °C |
| `4.3120` | Solar Setpoint ¹ | number | °C |
| `4.3376` | Whirlpool Setpoint ¹ | number | °C |
| `4.4001` | pH | sensor | — |
| `4.4008` | Cl | sensor | mg/l |
| `4.4022` | Redox | sensor | mV |
| `4.4033` | Water Temperature | sensor | °C |
| `4.4047` | Battery | sensor | V |
| `4.4069` | Air Temperature | sensor | °C |
| `4.4071` | Temperature T3 | sensor | °C |
| `4.4132` | Active Alarms | sensor | — |
| `5.5213` | Heating Mode | select | — |
| `5.5427` | Filter Pump Mode | select | — |
| `5.5433` | Out 1 ² | button | — |
| `5.5434` | Out 2 ² | button | — |
| `5.5435` | Out 3 ² | button | — |
| `5.5436` | Out 4 ² | button | — |
| `5.5485` | Out 5 ² | button | — |
| `5.5519` | Out 6 ² | button | — |
| `5.5553` | Out 7 ² | button | — |
| `5.5587` | Out 8 ² | button | — |
| `5.5621` | Out 9 ² | button | — |
| `5.5655` | Out 10 ² | button | — |
| `5.6012` | pH Pump Status | sensor | — |
| `5.6013` | Cl Pump Status | sensor | — |
| `5.6015` | Redox Pump Status | sensor | — |
| `5.6028` | Out 1 Status | sensor | — |
| `5.6029` | Out 2 Status | sensor | — |
| `5.6030` | Out 3 Status | sensor | — |
| `5.6031` | Out 4 Status | sensor | — |
| `5.6039` | Heating Status | sensor | — |
| `5.6058` | Out 5 Status | sensor | — |
| `5.6059` | Out 6 Status | sensor | — |
| `5.6060` | Out 7 Status | sensor | — |
| `5.6061` | Out 8 Status | sensor | — |
| `5.6062` | Out 9 Status | sensor | — |
| `5.6063` | Out 10 Status | sensor | — |
| `5.6064` | pH Canister Level | sensor | — |
| `5.6065` | pH Status | sensor | — |
| `5.6066` | Cl Canister Level | sensor | — |
| `5.6067` | pH System Status | sensor | — |
| `5.6068` | Redox Canister Level | sensor | — |
| `5.6069` | Redox Status | sensor | — |
| `5.6071` | Cl System Status | sensor | — |
| `5.6072` | Redox System Status | sensor | — |
| `5.6104` | Out 1 Available | sensor | — |
| `5.6105` | Out 2 Available | sensor | — |
| `5.6106` | Out 3 Available | sensor | — |
| `5.6107` | Out 4 Available | sensor | — |
| `5.6108` | Out 5 Available | sensor | — |
| `5.6109` | Out 6 Available | sensor | — |
| `5.6110` | Out 7 Available | sensor | — |
| `5.6111` | Out 8 Available | sensor | — |
| `5.6112` | Out 9 Available | sensor | — |
| `5.6113` | Out 10 Available | sensor | — |

¹ **Solar Setpoint** and **Whirlpool Setpoint** are disabled by default, because not every PM5 installation has a solar or whirlpool circuit.
To use them, go to Settings -> Devices & Services -> Bayrol -> Entities, open the entity and enable it. **Heating Setpoint** is enabled by default.

² Each `Out` entry creates three button entities: *On*, *Off* and *Auto* (for example `Out 1 On`, `Out 1 Off`, `Out 1 Auto`).
The current state of an output is reported by the matching `Out x Status` sensor, and `Out x Available` tells you whether the output is configured on the device.

### Filtering stale values when the pump is off

When the filter pump is not running, water does not circulate past the probes, so pH, redox and temperature readings become physically stale. The device keeps sending the last measured values anyway - the native Bayrol app shows them the same way, and this integration deliberately mirrors that behavior. Marking those sensors as *unavailable* would also clash with Home Assistant semantics, where *unavailable* means "the data source is broken" (e.g. MQTT connection lost), not "the value is old".

If you prefer gaps in your history instead of stale readings, you can build that per sensor with a standard [template sensor](https://www.home-assistant.io/integrations/template/), using the flow status entity this integration already provides. On Automatic SALT devices this is `Flow Contact` (the paddle switch on the FLOW input), which reports `On` while water is circulating and `Off` otherwise:

```yaml
template:
  - sensor:
      - name: "Pool pH (filtered)"
        unique_id: pool_ph_filtered
        state: >
          {% if is_state('sensor.bayrol_DEVICEID_flow_contact', 'On') %}
            {{ states('sensor.bayrol_DEVICEID_ph') }}
          {% else %}
            unknown
          {% endif %}
        availability: "{{ has_value('sensor.bayrol_DEVICEID_flow_contact') }}"
```

Replace `DEVICEID` with your device id - the exact entity ids are listed under Settings → Devices & Services → Bayrol. On devices without a `Flow Contact` entity, use `Flow Pump Status` instead and check which states it reports (Developer Tools → States). Repeat the pattern for redox and temperature if desired.

## Installation

### HACS (Recommended)

1. Make sure you have [HACS](https://hacs.xyz/) installed
2. Search for "Bayrol" and install the integration
3. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/bayrol_cloud` directory to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Configuration

1. Go to Settings -> Devices & Services
2. Click "Add Integration" and search for "Bayrol"
3. Enter your Bayrol App Link Code (found in the Bayrol Pool Access Web App)

## MQTT Debug

To debug MQTT messages from the Bayrol device, you can use [**MQTT Explorer**](http://mqtt-explorer.com).

### Step 1: Get your Access Token
First, obtain your **App Link Code** from the Bayrol Pool Access Web App.  
Replace the placeholder `A-aBcDeF` in the following URL with your code and open it in your browser:

https://www.bayrol-poolaccess.de/api/?code=A-aBcDeF

You will receive a response like this:

{"accessToken": "23154245abc693883ef23823","deviceSerial": "212ABC1-016273"}

Please note down both 'accessToken' and 'deviceSerial'.

### Step 2: Configure MQTT Explorer
In MQTT Explorer, enter the connection details as shown below.
Use your 'accessToken' value as the 'Username'.

<img width="654" height="438" alt="image" src="https://github.com/user-attachments/assets/bef549bb-e917-430b-bd07-79780a355f3d" />

### Step 3: Add Subscription
In **MQTT Explorer**, click the **ADVANCED** button and add the following subscription:

d02/`deviceSerial`>/v/#

For example, if your `deviceSerial` is `212ABC1-016273`, the subscription will be:

d02/212ABC1-016273/v/#

<img width="647" height="196" alt="image" src="https://github.com/user-attachments/assets/e3b17d01-4d21-4ac4-bb28-89ad07a5804d" />

### Step 4: Connect

Click the **CONNECT** button and you should see the messages floating in:

<img width="587" height="558" alt="image" src="https://github.com/user-attachments/assets/f92df652-5848-40ab-8edb-8250b50be68d" />


## Support

If you encounter any issues or have questions, please open an issue on GitHub.


