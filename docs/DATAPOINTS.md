# Bayrol PoolAccess MQTT datapoint reference

Community-maintained, unofficial reference of the MQTT datapoints published
by Bayrol PoolAccess devices, compiled from MQTT traffic observations and
device behavior. No guarantee of completeness, correctness or stability,
although the IDs have been stable across firmware updates so far (updates
added new IDs, existing ones did not change).

Topic scheme: the device publishes values on `d02/<device id>/v/<MQTT ID>`,
accepts writes on `d02/<device id>/s/<MQTT ID>` and answers value requests on
`d02/<device id>/g/<MQTT ID>` (see the [MQTT Debug](../README.md#mqtt-debug)
section of the README for how to explore this with MQTT Explorer).

The **Entity in HA** column shows the entity this integration already
creates for a datapoint. Descriptions marked with `*` are derived, the
device does not label these datapoints.

Missing something? [Open an issue](https://github.com/0xQuantumHome/bayrol-home-hassistant/issues),
known datapoints are usually quick to add. Please do not patch the
integration files locally, updates will overwrite local changes.

## 1. Automatic SALT / Automatic Cl-pH

Shared data model. The Device column is a heuristic: SALT covers the salt
electrolysis models (AS5/AS7), Cl-pH the liquid dosing models, "both"
applies to both.

### 1.1 Runtime values (149)

| MQTT ID | Description | Device | Entity in HA |
| --- | --- | --- | --- |
| `4.52` | Salt level warning | SALT | — |
| `4.53` | Cell protection mode, if salt level below | SALT | — |
| `4.54` | Cell protection mode, if temperature below | SALT | — |
| `4.78` | pH reading * | both | — |
| `4.80` | pH reading (pool measurement mode) * | both | — |
| `4.81` | pH reading (buffer calibration mode) * | both | — |
| `4.82` | Redox reading (salt electrolysis context) * | both | Redox (`sensor`) |
| `4.84` | Redox reading (filtered) * | both | — |
| `4.85` | Additional chlorine dosing: remaining time * | Cl-pH | — |
| `4.86` | Manual chlorine/redox dosing: remaining time * | both | — |
| `4.87` | Manual pH-Minus dosing: remaining time * | both | — |
| `4.88` | Manual pH-Plus dosing: remaining time * | both | — |
| `4.89` | Dosing | both | pH Dosing Rate (`sensor`) |
| `4.90` | Dosing | both | Cl Dosing Rate (`sensor`) |
| `4.91` | Production | SALT | Electrolyzer Production Rate (`sensor`) |
| `4.92` | Start delay remaining time | both | Start Delay Remaining (`sensor`) |
| `4.93` | Priming (suction): ready in * | both | — |
| `4.94` | Rinsing: ready in * | both | — |
| `4.95` | Additional chlorine dosing wait: ready in * | Cl-pH | — |
| `4.96` | pH dosing monitoring: cycle time * | both | — |
| `4.97` | Redox dosing monitoring: cycle time * | both | — |
| `4.98` | Temp. | both | Temperature (`sensor`) |
| `4.100` | Salt | SALT | Salt (`sensor`) |
| `4.102` | Conductivity | both | Conductivity (`sensor`) |
| `4.104` | Cell voltage | SALT | Electrolyzer Voltage (`sensor`) |
| `4.105` | Cell current | SALT | Electrolyzer Current (`sensor`) |
| `4.106` | Salt electrolysis cell power * | SALT | Cell Power (`sensor`) |
| `4.107` | Internal battery voltage | both | Battery Voltage (`sensor`) |
| `4.109` | Current software version * | both | — |
| `4.110` | Current software date code * | both | — |
| `4.111` | Stop production in | SALT | — |
| `4.112` | Next automatic polarity reversal in | SALT | Time Before Next Polarity Reversal (`sensor`) |
| `4.137` | Measured salt level in the pool | SALT | — |
| `4.138` | Amount of salt to add | SALT | Salt To Add (`sensor`) |
| `4.145` | Recommended min. daily filtration time | both | Recommended Min Daily Filtration Time (`sensor`) |
| `4.146` | Recommended production rate | SALT | Proposed Production Rate (`sensor`) |
| `4.147` | Estimated daily chlorine production | SALT | Estimated Daily Production (`sensor`) |
| `4.165` | Salt electrolysis switched off, if temperature below | SALT | — |
| `4.166` | Salt electrolysis switched off, if salt level below | SALT | — |
| `4.167` | Digital input: flow (BNC paddle switch) * | both | — |
| `4.168` | Digital input: pH canister level * | both | — |
| `4.169` | Digital input: cover contact * | both | — |
| `4.170` | Max. current A | both | — |
| `4.171` | Max. current B | both | — |
| `4.172` | Battery voltage (overview display) * | both | — |
| `4.182` | pH reading (pH-Minus context) * | both | pH (`sensor`) |
| `4.183` | pH reading (pH-Plus context) * | both | — |
| `4.184` | Salt reading (pH blocking screen) * | SALT | — |
| `4.185` | Conductivity reading (pH blocking screen) * | both | — |
| `4.186` | Last power off duration | both | — |
| `4.188` | Cell weighted operating hours ( time * % %) | SALT | — |
| `4.192` | pH reading with 0.01 resolution * | both | — |
| `4.196` | Desired production rate * | SALT | — |
| `4.204` | Redox reading * | both | — |
| `4.205` | Digital input: chlorine canister level * | Cl-pH | — |
| `4.206` | Digital input: flow (230V~ signal) * | both | — |
| `4.212` | No. of active messages | both | Message Count (`sensor`) |
| `4.214` | Conductivity ADC voltage | both | — |
| `4.215` | Gas alarm if < | both | — |
| `4.216` | Reset Gas alarm if > | both | — |
| `4.220` | Current temp. | both | — |
| `4.239` | RSSI signal strength (from Control Module) | both | WiFi RSSI (`sensor`) |
| `4.304` | Signal strength (must be at least 50%%) | both | Control Module Signal Strength (`sensor`) |
| `4.320` | Planned runtime today (Smart mode) | both | — |
| `4.321` | Actual runtime today | both | — |
| `4.322` | Average temperature | both | — |
| `4.324` | Salt electrolysis OFF > ON cycles (total) | SALT | — |
| `4.325` | Salt electrolysis OFF > ON cycles (today) | SALT | — |
| `4.326` | Salt electrolysis polarity reversals (total) | SALT | — |
| `4.327` | Salt electrolysis polarity reversals (today) | SALT | — |
| `4.337` | Max. chlorine dosing per day (l/m³) | Cl-pH | — |
| `4.338` | Max. chlorine dosing per day (active chlorine) | Cl-pH | — |
| `4.339` | Chlorine dosing amount today | Cl-pH | Cl Dosed Today (`sensor`) |
| `4.342` | Max. pH dosing per day (l/m³) | both | — |
| `4.343` | pH dosing amount today | both | pH Dosed Today (`sensor`) |
| `5.22` | pH status | both | — |
| `5.24` | Current pH dosing direction * | both | — |
| `5.25` | mV status (SE) | SALT | — |
| `5.27` | System state | both | — |
| `5.28` | 230V~ signal from the filter pump | both | Flow In 230V (`binary_sensor`) |
| `5.29` | Flow pump status * | both | Flow Pump Status (`sensor`) |
| `5.30` | Level input pH (BNC) | both | — |
| `5.31` | Level input chlorine (BNC) | both | — |
| `5.32` | Salt status | SALT | — |
| `5.33` | Temp. status | both | — |
| `5.34` | Salt electrolysis polarity mode * | SALT | — |
| `5.35` | Identified connected cell type | SALT | — |
| `5.36` | Pool cover contact (BNC) | both | — |
| `5.37` | Gas sensor | both | Gas Sensor (`binary_sensor`) |
| `5.38` | Salt electrolysis on/off state * | SALT | — |
| `5.44` | Current polarity | SALT | — |
| `5.45` | Ph status info * | both | — |
| `5.46` | Se status info * | SALT | — |
| `5.47` | Sys status * | both | — |
| `5.48` | Sys status info * | both | — |
| `5.73` | Ph value status * | both | — |
| `5.74` | Se value status * | SALT | — |
| `5.75` | T value status * | both | — |
| `5.76` | Salt value status * | SALT | — |
| `5.77` | Standby info * | both | — |
| `5.79` | Ph pump status * | both | — |
| `5.80` | pH-Minus canister | both | pH Minus Canister Status (`sensor`) |
| `5.81` | Salt electrolysis operating mode (auto/constant/boost/pause) * | SALT | — |
| `5.82` | Se polarity status * | SALT | — |
| `5.83` | Cover status * | both | Cover (`cover`) |
| `5.84` | T low status * | both | — |
| `5.85` | Se const * | SALT | — |
| `5.98` | Flow / paddle switch input (BNC) | both | Flow Contact (`binary_sensor`) |
| `5.118` | pH pump on/off state * | both | — |
| `5.123` | Plus+ cycle active | both | — |
| `5.124` | Safe mode production cycle active | both | — |
| `5.126` | Salt electrolysis Safe Mode active (after redox problem) * | SALT | — |
| `5.127` | Safe Mode production cycle currently running * | SALT | — |
| `5.128` | pH dosing operating mode (auto/manual/pause/off) * | both | — |
| `5.143` | pH-Plus canister | both | — |
| `5.144` | Redox monitoring status of the salt electrolysis * | SALT | — |
| `5.147` | Hardware version | both | HW Version (`sensor`) |
| `5.152` | WiFi status | both | WiFi State (`sensor`) |
| `5.153` | WiFi signal strength | both | WiFi Signal (`sensor`) |
| `5.165` | Chlorine pump on/off state * | both | — |
| `5.166` | Chlorine dosing operating mode (auto/manual/pause/off) * | both | — |
| `5.167` | mV status | both | — |
| `5.168` | Mv pump status * | both | — |
| `5.169` | Chlorine canister | both | Cl Canister Status (`sensor`) |
| `5.170` | Mv value status * | both | — |
| `5.171` | Mv status info * | both | — |
| `5.173` | Device type | both | Device Type (`sensor`) |
| `5.174` | Web portal status | both | Web Portal State (`sensor`) |
| `5.178` | Detected device type | both | Detected Device Type (`sensor`) |
| `5.190` | Vsp used * | both | — |
| `5.191` | Heating used * | both | — |
| `5.192` | Out1 used * | both | — |
| `5.193` | Out2 used * | both | — |
| `5.194` | Out3 used * | both | — |
| `5.195` | Out4 used * | both | — |
| `5.196` | Vsp speed * | both | — |
| `5.197` | Vsp on off * | both | — |
| `5.198` | Heating on off * | both | — |
| `5.199` | Out1 on off * | both | — |
| `5.200` | Out2 on off * | both | — |
| `5.201` | Out3 on off * | both | — |
| `5.202` | Out4 on off * | both | — |
| `5.203` | Control Module connection status * | both | — |
| `5.204` | Water treatment | both | — |
| `5.239` | Software update required | both | SW Update Required (`sensor`) |
| `5.242` | Connection quality | both | Control Module Connection Quality (`sensor`) |
| `5.260` | Control Module connection status (detailed) * | both | — |
| `5.275` | Flow input state (Flow in ON / Flow in OFF) * | both | Flow In Status (`binary_sensor`) |
| `5.277` | ESP32 version | both | — |

### 1.2 Settings (355)

| MQTT ID | Description | Device | Entity in HA |
| --- | --- | --- | --- |
| `4.1` | Undefined * | both | — |
| `4.2` | Desired pH level in the pool | both | pH Target (`number`) |
| `4.3` | Warning  message if pH reading above | both | pH Alert Max (`number`) |
| `4.4` | Warning  message if pH reading below | both | pH Alert Min (`number`) |
| `4.5` | Time interval for automatic pH monitoring | both | pH Dosing Control Time Interval (`sensor`) |
| `4.6` | pH measurement in the pool | both | — |
| `4.8` | Desired level of chlorine in the pool (DPD1) | Cl-pH | — |
| `4.9` | Current level of chlorine in the pool (DPD1) | Cl-pH | — |
| `4.10` | Pool volume | both | Pool Volume (`number`) |
| `4.11` | Pool temperature | both | — |
| `4.12` | Start chlorine dosing for | Cl-pH | — |
| `4.13` | Duration of the manual dosing | both | — |
| `4.14` | Increase chlorine level by | both | — |
| `4.15` | Duration of the manual dosing | both | — |
| `4.16` | Reduce pH level by | both | — |
| `4.17` | Duration of the manual dosing | both | — |
| `4.18` | Increase pH level by | both | — |
| `4.26` | Warning message if redox reading above | both | Redox Alert Max (`number`) |
| `4.27` | Warning message if redox reading below | both | Redox Alert Min (`number`) |
| `4.28` | Setpoint for redox control | both | Redox Target (`number`) |
| `4.29` | Time interval for redox monitoring | both | — |
| `4.30` | Approximation for redox monitoring | both | — |
| `4.32` | Dosing capacity of the pH pump | both | — |
| `4.33` | Dosing capacity of the chlorine pump | both | — |
| `4.34` | Approximation for automatic pH monitoring | both | Minimal Approach to Control the pH (`sensor`) |
| `4.35` | Desired pH pump runtime | both | — |
| `4.36` | Rinse time | both | — |
| `4.37` | Start delay | both | Start Delay (`number`) |
| `4.38` | Dosing cycle (pump ON/OFF time) | both | pH Dosing Cycle (`sensor`) |
| `4.39` | Dosing cycle (pump ON/OFF time) | both | — |
| `4.44` | Accept redox reading as setpoint | both | — |
| `4.47` | Adjust 'normal' dosing amount (pH) | both | pH Dosing Speed (`sensor`) |
| `4.48` | Adjust 'normal' production level | both | — |
| `4.51` | Polarity change after | SALT | Polarity Reversal Times (`sensor`) |
| `4.66` | Minimum production rate when ON | SALT | Minimum Redox Produktion (`number`) |
| `4.67` | Sw version * | both | SW Version (`sensor`) |
| `4.68` | Sw date * | both | SW Date (`sensor`) |
| `4.69` | time.hours | both | Hourly Counter / Reset every 24h (`sensor`) |
| `4.70` | time.minutes | both | — |
| `4.71` | time.seconds | both | — |
| `4.72` | date.day | both | — |
| `4.73` | date.month | both | — |
| `4.74` | date.year | both | — |
| `4.75` | Production rate in Constant mode | SALT | — |
| `4.77` | Stop time-limited production after | SALT | — |
| `4.113` | Store logging data every | both | — |
| `4.114` | Max. current 5-plates cell | both | — |
| `4.115` | Max. current 7-plates cell | both | — |
| `4.116` | Stop time-limited dosing after | both | — |
| `4.117` | Stop time-limited dosing at a pH value of | both | — |
| `4.118` | Desired redox range / minimum | both | — |
| `4.119` | Time since last polarity reversal | SALT | Time Since Polarity Reversal (`sensor`) |
| `4.120` | Cell operating hours | SALT | — |
| `4.121` | Cell operating hours (polarity A) | SALT | — |
| `4.122` | Cell operating hours (polarity B) | SALT | — |
| `4.123` | Desired temp. | both | — |
| `4.124` | T upper limit * | both | — |
| `4.125` | Chlorine increase by daily plus+ cycle | SALT | — |
| `4.131` | View = user / edit = user | both | — |
| `4.132` | View = user / edit = service | both | — |
| `4.133` | View, edit = customer_iel | both | — |
| `4.141` | Production rate factor when pool cover is closed | SALT | — |
| `4.143` | Daily filtration time | both | — |
| `4.144` | Preferred salt level in the pool | SALT | Salt Preferred Level (`number`) |
| `4.148` | Desired daily chlorine production in safe mode | SALT | — |
| `4.149` | Production rate | SALT | — |
| `4.150` | Stop time-limited production at a redox value of | SALT | — |
| `4.151` | This item should be invisible | both | — |
| `4.158` | Accepted drop of the redox reading (dead zone) | both | — |
| `4.159` | Stop plus+ cycles if redox exceeds setpoint by | both | — |
| `4.160` | Display on level | both | — |
| `4.161` | Display dimming level | both | — |
| `4.162` | Chlorine increase by weekly plus+ cycle | SALT | — |
| `4.163` | Pool volume | both | — |
| `4.164` | Preferred salt level in the pool | SALT | — |
| `4.173` | Cell average production rate | both | — |
| `4.174` | Production rate 5-plates cell | both | — |
| `4.175` | Production rate 7-plates cell | both | — |
| `4.176` | Device total operating hours | both | Power On Time (`sensor`) |
| `4.177` | Cell weighted operating hours (pol. A) | SALT | — |
| `4.178` | Cell weighted operating hours (pol. B) | SALT | — |
| `4.179` | Plus+ cycle timer | SALT | — |
| `4.180` | Current Polarity 0/1 | SALT | — |
| `4.181` | Gas detection sensitivity | both | — |
| `4.187` | Ram function status * | both | — |
| `4.189` | Redox monitoring timer (setpoint) | both | — |
| `4.190` | Timestamp lower 16 bits | both | — |
| `4.191` | Timestamp upper 16 bits | both | — |
| `4.193` | Redox monitoring timer (rise) | both | — |
| `4.194` | Redox monitoring active timer (setpoint) | both | — |
| `4.195` | Redox monitoring active timer (rise) | both | — |
| `4.197` | ADC1 correction from old to new config. | both | — |
| `4.201` | Stop time-limited dosing after | both | — |
| `4.202` | Stop time-limited dosing at a redox value of | both | — |
| `4.209` | Adjust 'normal' dosing amount (redox) | both | — |
| `4.213` | Salt electrolysis switched off, if temperature below | SALT | — |
| `4.217` | Dosing capacity of the pH pump | both | — |
| `4.218` | Dosing capacity of the chlorine pump | both | — |
| `4.221` | Start time | both | — |
| `4.222` | Stop time | both | — |
| `4.223` | Days of week | both | — |
| `4.224` | Start time | both | — |
| `4.225` | Stop time | both | — |
| `4.226` | Days of week | both | — |
| `4.227` | Start time | both | — |
| `4.228` | Stop time | both | — |
| `4.229` | Days of week | both | — |
| `4.230` | Start time | both | — |
| `4.231` | Stop time | both | — |
| `4.232` | Days of week | both | — |
| `4.233` | Start time | both | — |
| `4.234` | Stop time | both | — |
| `4.235` | Days of week | both | — |
| `4.236` | Start time | both | — |
| `4.237` | Stop time | both | — |
| `4.238` | Days of week | both | — |
| `4.241` | Start time | both | — |
| `4.242` | Stop time | both | — |
| `4.243` | Days of week | both | — |
| `4.244` | Start time | both | — |
| `4.245` | Stop time | both | — |
| `4.246` | Days of week | both | — |
| `4.247` | Start time | both | — |
| `4.248` | Stop time | both | — |
| `4.249` | Days of week | both | — |
| `4.250` | Start time | both | — |
| `4.251` | Stop time | both | — |
| `4.252` | Days of week | both | — |
| `4.253` | Start time | both | — |
| `4.254` | Stop time | both | — |
| `4.255` | Days of week | both | — |
| `4.256` | Start time | both | — |
| `4.257` | Stop time | both | — |
| `4.258` | Days of week | both | — |
| `4.259` | Start time | both | — |
| `4.260` | Stop time | both | — |
| `4.261` | Days of week | both | — |
| `4.262` | Start time | both | — |
| `4.263` | Stop time | both | — |
| `4.264` | Days of week | both | — |
| `4.265` | Start time | both | — |
| `4.266` | Stop time | both | — |
| `4.267` | Days of week | both | — |
| `4.268` | Light program | both | — |
| `4.269` | Light program | both | — |
| `4.270` | Light program | both | — |
| `4.271` | Light program | both | — |
| `4.272` | Light program | both | — |
| `4.273` | Light program | both | — |
| `4.274` | Light program | both | — |
| `4.275` | Light program | both | — |
| `4.276` | Light program | both | — |
| `4.277` | Light program | both | — |
| `4.278` | Light program | both | — |
| `4.279` | Light program | both | — |
| `4.280` | Program RESET ON time | both | — |
| `4.281` | Program RESET OFF time | both | — |
| `4.282` | NEXT program ON time | both | — |
| `4.283` | NEXT program OFF time | both | — |
| `4.284` | Program RESET ON time | both | — |
| `4.285` | Program RESET OFF time | both | — |
| `4.286` | NEXT program ON time | both | — |
| `4.287` | NEXT program OFF time | both | — |
| `4.288` | Program RESET ON time | both | — |
| `4.289` | Program RESET OFF time | both | — |
| `4.290` | NEXT program ON time | both | — |
| `4.291` | NEXT program OFF time | both | — |
| `4.292` | Program RESET ON time | both | — |
| `4.293` | Program RESET OFF time | both | — |
| `4.294` | NEXT program ON time | both | — |
| `4.295` | NEXT program OFF time | both | — |
| `4.296` | Accepted deviation (hysteresis) | both | — |
| `4.297` | Activate frost protection if water temp. below | both | — |
| `4.298` | Accepted deviation (hysteresis) | both | — |
| `4.299` | Min. pump runtime  in frost protection | both | — |
| `4.300` | Pump start time in Smart mode | both | — |
| `4.303` | Daily pump runtime in winter mode (< 12°C)  [hh:mm] | both | — |
| `4.305` | Test light program | both | — |
| `4.306` | Test light program | both | — |
| `4.307` | Test light program | both | — |
| `4.308` | Test light program | both | — |
| `4.309` | Blocking start time | both | — |
| `4.310` | Blocking stop time | both | — |
| `4.311` | Days of week | both | — |
| `4.312` | Blocking start time | both | — |
| `4.313` | Blocking stop time | both | — |
| `4.314` | Days of week | both | — |
| `4.315` | Blocking start time | both | — |
| `4.316` | Blocking stop time | both | — |
| `4.317` | Days of week | both | — |
| `4.318` | Ram pump smart runtime in s * | both | — |
| `4.319` | Pump smart date code * | both | — |
| `4.335` | Chlorine dosing time today | Cl-pH | Cl Dosing Time Today (`sensor`) |
| `4.336` | Max. chlorine dosing per day | Cl-pH | Cl Daily Dosing Limit (`number`) |
| `4.340` | pH dosing time today | both | pH Dosing Time Today (`sensor`) |
| `4.341` | Max. pH dosing per day | both | pH Daily Dosing Limit (`number`) |
| `4.344` | Out of range error: Lower limit | both | — |
| `4.345` | Out of range error: Delay time | both | — |
| `4.346` | Out of range error: Lower limit | both | — |
| `4.347` | Out of range error: Upper limit | both | — |
| `4.348` | Out of range error: Delay time | both | — |
| `4.354` | Last * | both | — |
| `5.1` | Undefined * | both | — |
| `5.2` | Menu language | both | Language (`sensor`) |
| `5.3` | Adjust pH dosing amount | both | pH Production Rate (`select`) |
| `5.4` | Increase dos. amount | both | — |
| `5.5` | Adjust salt electrolysis production level | SALT | — |
| `5.6` | Increase salt electrolysis production level | SALT | — |
| `5.8` | Product used for pH dosing | both | — |
| `5.9` | Acoustic alarm signal in case of messages | both | Alarm Sound (`sensor`) |
| `5.10` | Controller type (temporary for demo) | both | — |
| `5.11` | Paddle switch on FLOW input (BNC) | both | — |
| `5.12` | Level switch in the pH canister | both | — |
| `5.13` | Level switch in the Cl canister | both | — |
| `5.15` | Redox setpoint adjusted? | both | — |
| `5.16` | Simulate measurement readings | both | — |
| `5.17` | Polarity | SALT | SE Polarity (`sensor`) |
| `5.18` | Add cl method * | Cl-pH | — |
| `5.19` | Select Software update option | both | — |
| `5.20` | Automatic operation | both | — |
| `5.21` | Continuous operation | SALT | — |
| `5.39` | Dosing direction mV | both | — |
| `5.40` | Salt electrolysis ON/OFF | SALT | Salt electrolysis ON/OFF (`switch`) |
| `5.41` | Salt electrolysis operating mode | SALT | Redox Mode (`select`) |
| `5.42` | Automatic pH dosing ON/OFF | both | pH Dosing ON/OFF (`switch`) |
| `5.43` | Connected cell type | SALT | — |
| `5.49` | Day of week for the weekly plus+ cycle | SALT | — |
| `5.50` | Stop salt electrolysis if temperature low | SALT | — |
| `5.51` | Stop electrolysis if salt level low | SALT | — |
| `5.52` | Show filtration on/off | both | — |
| `5.53` | Show alarms | both | — |
| `5.54` | Show calibrations | both | — |
| `5.55` | Show user input (parameter settings) | both | — |
| `5.56` | Show other events | both | — |
| `5.57` | Simulate Safe Mode / Stopped messages | both | — |
| `5.58` | Switch on pH pump for 1 minute | both | — |
| `5.59` | Pause pH dosing for | both | pH Pause Runtime (`sensor`) |
| `5.60` | Pause salt electrolysis for | SALT | SE Pause Runtime (`sensor`) |
| `5.61` | Pause pH dosing also | both | — |
| `5.62` | Pause salt electrolysis also | both | — |
| `5.63` | Duration of BOOST mode | SALT | — |
| `5.68` | View = user / edit = user | both | — |
| `5.69` | View = user / edit = service | both | — |
| `5.70` | View, edit = customer_iel | both | — |
| `5.86` | Run commissioning wizard at next system start | both | — |
| `5.89` | Switch on salt electrolysis | both | — |
| `5.90` | Login for context menus | both | — |
| `5.91` | Activate auto login | both | — |
| `5.92` | System overview | both | — |
| `5.93` | Pool cover switch | both | — |
| `5.94` | If a redox problem is detected | SALT | — |
| `5.95` | If a pH problem is detected | both | — |
| `5.96` | Redox setpoint monitoring | both | — |
| `5.97` | Redox reaction monitoring | both | — |
| `5.99` | Activate 'Add salt' wizard | SALT | — |
| `5.100` | Daily or weekly plus+ cycles | SALT | — |
| `5.101` | Additional plus+ cycles every day | SALT | — |
| `5.102` | Run pH pump for the selected time | both | — |
| `5.107` | Auto login user level | both | — |
| `5.110` | Stop dosing when setpoint is reached | both | — |
| `5.111` | Stop production when setpoint is reached | SALT | — |
| `5.112` | Never stop plus+ cycles (not recommended) | SALT | — |
| `5.113` | If a redox problem is detected | SALT | — |
| `5.114` | Confirm correct chlorine level in the pool | Cl-pH | — |
| `5.115` | Automatic summer/winter time changeover | both | — |
| `5.116` | Show info message, when salt level drops | SALT | — |
| `5.117` | SE cycle | SALT | — |
| `5.145` | ADC1 correction from old to new config. set | both | — |
| `5.146` | Is summertime * | both | — |
| `5.149` | Expert Mode at system start | both | — |
| `5.150` | Activate WiFi | both | — |
| `5.151` | DHCP (automatic configuration) | both | — |
| `5.154` | Automatic chlorine dosing ON/OFF | both | Cl Dosing ON/OFF (`switch`) |
| `5.159` | Run chlorine pump for the selected time | both | — |
| `5.160` | Pause chlorine dosing for | both | — |
| `5.161` | Pause chlorine dosing also | both | — |
| `5.164` | Switch on chlorine pump for 1 minute | both | — |
| `5.172` | Device type | both | — |
| `5.175` | Adjust chlorine dosing amount | both | Cl Adjust Dosing Amount (`select`) |
| `5.176` | Temperature sensor | both | — |
| `5.180` | Last detected device type | both | — |
| `5.183` | Device has 6l/h pumps | both | — |
| `5.184` | Filtration mode | both | Filtration mode (`select`) |
| `5.185` | Heating mode (auto/off) | both | — |
| `5.186` | Operating mode (auto/on/off) | both | Out 1 Mode (`select`) |
| `5.187` | Operating mode (auto/on/off) | both | Out 2 Mode (`select`) |
| `5.188` | Operating mode (auto/on/off) | both | Out 3 Mode (`select`) |
| `5.189` | Operating mode (auto/on/off) | both | Out 4 Mode (`select`) |
| `5.205` | Connect Smart&Easy Control Module | both | — |
| `5.206` | Activate timer | both | — |
| `5.207` | Pump speed | both | — |
| `5.208` | Activate timer | both | — |
| `5.209` | Pump speed | both | — |
| `5.210` | Activate timer | both | — |
| `5.211` | Pump speed | both | — |
| `5.212` | Activate timer | both | — |
| `5.213` | Activate timer | both | — |
| `5.214` | Activate timer | both | — |
| `5.215` | Use variable speed pump | both | — |
| `5.216` | Extend pump runtime at high temp. | both | — |
| `5.217` | OUT 1 function | both | — |
| `5.218` | OUT 2 function | both | — |
| `5.219` | OUT 3 function | both | — |
| `5.220` | OUT 4 function | both | — |
| `5.222` | Clock timer enabled | both | — |
| `5.223` | Clock timer enabled | both | — |
| `5.224` | Clock timer enabled | both | — |
| `5.225` | Clock timer enabled | both | — |
| `5.226` | Clock timer enabled | both | — |
| `5.227` | Clock timer enabled | both | — |
| `5.228` | Clock timer enabled | both | — |
| `5.229` | Clock timer enabled | both | — |
| `5.230` | Clock timer enabled | both | — |
| `5.231` | "No flow" blocks output | both | — |
| `5.232` | "No flow" blocks output | both | — |
| `5.233` | "No flow" blocks output | both | — |
| `5.234` | "No flow" blocks output | both | — |
| `5.235` | Click here for colour change | both | — |
| `5.236` | Click here for colour change | both | — |
| `5.237` | Click here for colour change | both | — |
| `5.238` | Click here for colour change | both | — |
| `5.240` | Touch beep | both | — |
| `5.241` | Synchronize time with Web | both | — |
| `5.243` | Heat when pump speed low | both | — |
| `5.244` | Heat when pump speed med | both | — |
| `5.245` | Heat when pump speed high | both | — |
| `5.246` | Dosing when pump speed low | both | — |
| `5.247` | Dosing when pump speed med | both | — |
| `5.248` | Dosing when pump speed high | both | — |
| `5.249` | Pump speed in Smart mode | both | — |
| `5.250` | Pump speed in Winter mode | both | — |
| `5.251` | Pump speed in frost protection mode | both | — |
| `5.252` | Activate frost protection | both | — |
| `5.253` | Select configuration | both | — |
| `5.254` | Force filter pump ON during BOOST mode | both | — |
| `5.255` | Keep existing configuration of switching functions | both | — |
| `5.256` | Filtration mode | both | — |
| `5.257` | I am using a Smart&Easy Box | both | — |
| `5.258` | My pool light can be controlled by power breaks | both | — |
| `5.259` | Last Home screen | both | — |
| `5.261` | OUT 1 function | both | — |
| `5.262` | OUT 2 function | both | — |
| `5.263` | OUT 3 function | both | — |
| `5.264` | OUT 4 function | both | — |
| `5.265` | Set e_c_fm_supported | both | — |
| `5.266` | Set e_c_fm_used | both | — |
| `5.267` | Blocking clock timer enabled | both | — |
| `5.268` | Blocking clock timer enabled | both | — |
| `5.269` | Blocking clock timer enabled | both | — |
| `5.270` | Pump speed in BOOST mode | both | — |
| `5.271` | Filtration mode | both | — |
| `5.272` | Filtration mode | both | — |
| `5.273` | Heat when pump OFF & flow signal ON | both | — |
| `5.274` | Dosing when pump OFF & flow signal ON | both | — |
| `5.280` | Last * | both | — |

### 1.3 Internal (calibration, tests, GUI helpers; not recommended to implement, 123)

<details><summary>expand</summary>

| MQTT ID | Description | Device | Entity in HA |
| --- | --- | --- | --- |
| `4.7` | pH value of the buffer solution | both | Minutes Counter / Reset every hour (`sensor`) |
| `4.19` | HW calibration pH offset | both | — |
| `4.20` | HW calibration pH factor | both | — |
| `4.21` | pH calibration offset | both | — |
| `4.22` | pH electrode slope | both | — |
| `4.23` | HW calibration mV offset | both | — |
| `4.24` | HW calibration mV factor | both | — |
| `4.25` | Redox calibration offset | both | — |
| `4.31` | Redox value of the buffer solution | both | — |
| `4.40` | Base p-range pH ( 40m³ / 2.2l/h / normal ) | both | — |
| `4.41` | Base p-range mV ( 40m³ / 13g/h / normal ) | both | — |
| `4.42` | Base min. dos. pH ( 40m³ / 2.2l/h / normal ) | both | — |
| `4.43` | Base min. dos. mV ( 40m³ / 13g/h / normal ) | SALT | — |
| `4.45` | Base man. dos. pH ( 10m³ / 2,2l/h / 0,1pH ) | both | — |
| `4.46` | Base man. dos. Cl ( 10m³ /  13g/h / 0,1mg/l ) | both | — |
| `4.49` | Pool temperature (thermometer) | both | — |
| `4.55` | Real salt level in the pool | SALT | — |
| `4.56` | Salt measurement calibration offset | SALT | — |
| `4.57` | Conductivity in the pool (manual measurement) | both | — |
| `4.58` | Conductivity calibration offset | both | — |
| `4.59` | Temperature calibration offset | both | — |
| `4.60` | HW calibration offset temperature | both | — |
| `4.61` | HW calibration factor temperature | both | — |
| `4.62` | HW calibration offset conductivity | both | — |
| `4.63` | HW calibration factor conductivity | both | — |
| `4.64` | Production rate salt electrolysis | SALT | — |
| `4.79` | Current pH reading | both | — |
| `4.83` | Current redox reading | both | — |
| `4.99` | Current temperature reading | both | — |
| `4.101` | Current salt level reading | SALT | — |
| `4.103` | Current conductivity reading | both | — |
| `4.108` | Polarity reversal in | SALT | — |
| `4.126` | Progress bar 0-100%% | both | — |
| `4.127` | Progress bar time in [s] | both | — |
| `4.128` | Progress bar time in [min] | both | — |
| `4.129` | View = guest / edit = guest | both | — |
| `4.130` | View = guest / edit = user | both | — |
| `4.134` | var: view = guest | both | — |
| `4.135` | var: view = user | both | — |
| `4.136` | Production time salt electrolysis | SALT | — |
| `4.139` | pH pump runtime progress | both | — |
| `4.140` | Measurement in progress…. | both | — |
| `4.142` | Measurement in progress…. | both | — |
| `4.152` | pH time-limited dosing progress | both | — |
| `4.153` | pH pause elapsed time | both | — |
| `4.155` | BOOST mode elapsed time | SALT | — |
| `4.156` | Time-limited production progress | SALT | — |
| `4.157` | Salt electrolysis pause elapsed time | SALT | — |
| `4.198` | ADC1 calibration offset | both | — |
| `4.199` | Time-limited dosing progress | both | — |
| `4.200` | Pause elapsed time | both | — |
| `4.203` | Chlorine pump runtime progress | both | — |
| `4.207` | Base p-range mV ( 40m³ / 2.2l/h / normal ) | both | — |
| `4.208` | Base min. dos. mV ( 40m³ / 2.2l/h / normal ) | both | — |
| `4.210` | Base man. dos. Cl ( 10m³ /  2,2l/h / 0,1mg/l ) | both | — |
| `4.211` | No. of Eventlog events | both | — |
| `4.219` | HW calibration offset conductivity v1.60 | both | — |
| `4.240` | Local time = UTC + this offset | both | — |
| `4.323` | Clock time correction per 24 hours | both | — |
| `4.328` | Salt electrolysis refresh cycles (total) | SALT | — |
| `4.329` | Salt electrolysis refresh cycles (today) | SALT | — |
| `4.330` | Salt electrolysis failed refresh cycles (total) | SALT | — |
| `4.331` | Cycle ON time | SALT | — |
| `4.332` | Cycle OFF time | SALT | — |
| `4.333` | No. of cycles | SALT | — |
| `4.334` | Target state ( 0=OFF / 1=ON ) | SALT | — |
| `4.349` | Accelerated polarity change for testing after | SALT | — |
| `4.350` | Number of retries for refresh cycles | SALT | — |
| `4.351` | Delay before fault detection | SALT | — |
| `4.352` | Verification delay after relay_switching | SALT | — |
| `4.353` | Verification delay after refresh cycles | SALT | — |
| `5.7` | Regional standard settings for | both | — |
| `5.14` | Run commissioning wizard at next system start | both | — |
| `5.23` | Ph status display * | both | — |
| `5.26` | Mv status display * | both | — |
| `5.64` | View = guest / edit = guest | both | — |
| `5.65` | View = guest / edit = service | both | — |
| `5.66` | View = guest / edit = guest | both | — |
| `5.67` | View = guest / edit = user | both | — |
| `5.71` | var: view = guest | both | — |
| `5.72` | var: view = user | both | — |
| `5.78` | Ph opmode icon * | both | — |
| `5.87` | Endtest (manual) at system start | both | — |
| `5.88` | Endtest (auto) at system start | both | — |
| `5.103` | Pool measurement or buffer solution? | both | — |
| `5.104` | Activate BOOST mode | SALT | — |
| `5.105` | Activate time-limited constant production | SALT | — |
| `5.106` | Pause salt electrolysis | SALT | — |
| `5.108` | Activate time-limited pH dosing | both | — |
| `5.109` | Pause pH dosing | both | — |
| `5.119` | Gui run init * | both | — |
| `5.120` | Se test running * | SALT | — |
| `5.121` | Enable endtest auto * | both | — |
| `5.122` | SE blocked | SALT | — |
| `5.125` | Se opmode icon * | SALT | — |
| `5.129` | Gui no pin code * | both | — |
| `5.130` | Se activate boost * | SALT | — |
| `5.131` | Se activate manual * | SALT | — |
| `5.132` | Se activate pause * | SALT | — |
| `5.133` | Ph activate manual * | both | — |
| `5.134` | Ph activate pause * | both | — |
| `5.135` | Activate BOOST mode | SALT | — |
| `5.136` | Activate time-limited constant production | SALT | — |
| `5.137` | Pause salt electrolysis | SALT | — |
| `5.138` | Activate time-limited pH dosing | both | — |
| `5.139` | Pause pH dosing | both | — |
| `5.140` | Accelerate timers for testing | both | — |
| `5.141` | Ph blocked by salt * | SALT | — |
| `5.142` | Ph blocked * | both | — |
| `5.148` | Activate data logging on USB stick | both | — |
| `5.155` | Activate time-limited chlorine dosing | both | — |
| `5.156` | Activate time-limited chlorine dosing | both | — |
| `5.157` | Pause chlorine dosing | both | — |
| `5.158` | Pause chlorine dosing | both | — |
| `5.162` | Mv activate manual * | both | — |
| `5.163` | Mv activate pause * | both | — |
| `5.177` | Mv opmode icon * | both | — |
| `5.179` | Mv blocked * | both | — |
| `5.181` | Resend all MQTT topics | both | — |
| `5.221` | Local time offset valid | both | — |
| `5.276` | New calibration of the clock | both | — |
| `5.278` | Run relay stress test (switch every second) | both | — |
| `5.279` | Simulate relay fault | both | — |

</details>

## 2. Pool Manager 5 (PM5)

### 2.1 Datapoints (124)

| MQTT ID | Description | Entity in HA |
| --- | --- | --- |
| `4.3001` | Ph setpoint | pH Target (`select`) |
| `4.3002` | Ph lower al | pH Alert Min (`select`) |
| `4.3003` | Ph upper al | pH Alert Max (`select`) |
| `4.3017` | Cl setpoint | Setpoint Chlorine (`select`) |
| `4.3018` | Cl lower al | Lower Alarm threshold Chlorine (`select`) |
| `4.3019` | Cl upper al | Upper Alarm threshold Chlorine (`select`) |
| `4.3033` | Br setpoint | — |
| `4.3034` | Br lower al | — |
| `4.3035` | Br upper al | — |
| `4.3049` | Mv setpoint cl | Setpoint Redox (`select`) |
| `4.3050` | Mv setpoint br | — |
| `4.3051` | Mv lower al cl | Redox Alert Min (`select`) |
| `4.3052` | Mv lower al br | — |
| `4.3053` | Mv upper al cl | Redox Alert Max (`select`) |
| `4.3054` | Mv upper al br | — |
| `4.3069` | T1 lower al | — |
| `4.3070` | T1 upper al | — |
| `4.3074` | T2 lower al | — |
| `4.3075` | T2 upper al | — |
| `4.3079` | T3 lower al | — |
| `4.3080` | T3 upper al | — |
| `4.3084` | O2 amount | — |
| `4.3118` | Heating setpoint | Heating Setpoint (`number`) |
| `4.3120` | Solar setpoint | Solar Setpoint (`number`) |
| `4.3376` | Whirlpool setpoint | Whirlpool Setpoint (`number`) |
| `4.4001` | Ph | pH (`sensor`) |
| `4.4008` | Cl | Cl (`sensor`) |
| `4.4015` | Br | — |
| `4.4022` | Mv | Redox (`sensor`) |
| `4.4027` | O2 dosed amount | — |
| `4.4033` | T1 | Water Temperature (`sensor`) |
| `4.4047` | Battery | Battery (`sensor`) |
| `4.4069` | T2 | Air Temperature (`sensor`) |
| `4.4071` | T3 | Temperature T3 (`sensor`) |
| `4.4129` | Btc | — |
| `4.4132` | No of active alarms | Active Alarms (`sensor`) |
| `4.4133` | Mqtt test messages | — |
| `5.5017` | Ph op mode | — |
| `5.5018` | Cl op mode | — |
| `5.5019` | Br op mode | — |
| `5.5020` | Mv op mode | — |
| `5.5021` | O2 op mode | — |
| `5.5041` | O2 t comp | — |
| `5.5184` | Pump mode 1 | — |
| `5.5185` | Pump mode 2 | — |
| `5.5186` | Pump mode 3 | — |
| `5.5187` | Pump mode 4 | — |
| `5.5188` | Pump mode 5 | — |
| `5.5189` | Pump mode 6 | — |
| `5.5213` | Heating mode | Heating Mode (`select`) |
| `5.5215` | Heating t input | — |
| `5.5224` | Solar mode | — |
| `5.5294` | T1 function | — |
| `5.5295` | T2 function | — |
| `5.5296` | T3 function | — |
| `5.5427` | Pump eco normal high | Filter Pump Mode (`select`) |
| `5.5433` | Out1 buttons | Out 1 (`button`) |
| `5.5434` | Out2 buttons | Out 2 (`button`) |
| `5.5435` | Out3 buttons | Out 3 (`button`) |
| `5.5436` | Out4 buttons | Out 4 (`button`) |
| `5.5464` | Out4 whirlpool buttons | — |
| `5.5485` | Out5 buttons | Out 5 (`button`) |
| `5.5519` | Out6 buttons | Out 6 (`button`) |
| `5.5553` | Out7 buttons | Out 7 (`button`) |
| `5.5587` | Out8 buttons | Out 8 (`button`) |
| `5.5621` | Out9 buttons | Out 9 (`button`) |
| `5.5655` | Out10 buttons | Out 10 (`button`) |
| `5.6012` | Ph pump on | pH Pump Status (`sensor`) |
| `5.6013` | Cl pump on | Cl Pump Status (`sensor`) |
| `5.6014` | Br pump on | — |
| `5.6015` | Mv pump on | Redox Pump Status (`sensor`) |
| `5.6016` | O2 pump on | — |
| `5.6028` | Out1 on off | Out 1 Status (`sensor`) |
| `5.6029` | Out2 on off | Out 2 Status (`sensor`) |
| `5.6030` | Out3 on off | Out 3 Status (`sensor`) |
| `5.6031` | Out4 on off | Out 4 Status (`sensor`) |
| `5.6039` | Heating on off | Heating Status (`sensor`) |
| `5.6040` | Solar on off | — |
| `5.6058` | Out5 on off | Out 5 Status (`sensor`) |
| `5.6059` | Out6 on off | Out 6 Status (`sensor`) |
| `5.6060` | Out7 on off | Out 7 Status (`sensor`) |
| `5.6061` | Out8 on off | Out 8 Status (`sensor`) |
| `5.6062` | Out9 on off | Out 9 Status (`sensor`) |
| `5.6063` | Out10 on off | Out 10 Status (`sensor`) |
| `5.6064` | Ph canister level | pH Canister Level (`sensor`) |
| `5.6065` | Ph status | pH Status (`sensor`) |
| `5.6066` | Cl canister level | Cl Canister Level (`sensor`) |
| `5.6067` | Cl status | pH System Status (`sensor`) |
| `5.6068` | Mv canister level | Redox Canister Level (`sensor`) |
| `5.6069` | Mv status | Redox Status (`sensor`) |
| `5.6070` | O2 canister level | — |
| `5.6071` | O2 status | Cl System Status (`sensor`) |
| `5.6072` | Br status | Redox System Status (`sensor`) |
| `5.6083` | Pump current speed | Filter Pump Current Speed (`sensor`) |
| `5.6084` | Pump available speeds | — |
| `5.6085` | Btc status | — |
| `5.6086` | Btc current mode | — |
| `5.6088` | Whirlpool on off | — |
| `5.6089` | Whirlpool heating on off | — |
| `5.6090` | Ph available | — |
| `5.6091` | Cl available | — |
| `5.6092` | Br available | — |
| `5.6093` | Mv measure available | — |
| `5.6094` | Mv dosing cl available | — |
| `5.6095` | O2 available | — |
| `5.6096` | T1 available | — |
| `5.6097` | T2 available | — |
| `5.6098` | T3 available | — |
| `5.6099` | Heating available | — |
| `5.6100` | Solar available | — |
| `5.6101` | Pump available | — |
| `5.6102` | Btc available | — |
| `5.6104` | Out1 available | Out 1 Available (`sensor`) |
| `5.6105` | Out2 available | Out 2 Available (`sensor`) |
| `5.6106` | Out3 available | Out 3 Available (`sensor`) |
| `5.6107` | Out4 available | Out 4 Available (`sensor`) |
| `5.6108` | Out5 available | Out 5 Available (`sensor`) |
| `5.6109` | Out6 available | Out 6 Available (`sensor`) |
| `5.6110` | Out7 available | Out 7 Available (`sensor`) |
| `5.6111` | Out8 available | Out 8 Available (`sensor`) |
| `5.6112` | Out9 available | Out 9 Available (`sensor`) |
| `5.6113` | Out10 available | Out 10 Available (`sensor`) |
| `5.6114` | Whirlpool available | — |
| `5.6117` | Mv dosing br available | — |

### 2.2 Timer configuration blocks (120)

Schedule configuration for the pump and Out 1-10 (six timers each with
active flag and weekdays). Of little use in Home Assistant.

<details><summary>expand</summary>

| MQTT ID | Description | Entity in HA |
| --- | --- | --- |
| `5.5046` | Out1 day of week 1 | — |
| `5.5047` | Out1 day of week 2 | — |
| `5.5048` | Out1 day of week 3 | — |
| `5.5049` | Out2 day of week 1 | — |
| `5.5050` | Out2 day of week 2 | — |
| `5.5051` | Out2 day of week 3 | — |
| `5.5121` | Out4 day of week 1 | — |
| `5.5122` | Out4 day of week 2 | — |
| `5.5123` | Out4 day of week 3 | — |
| `5.5203` | Pump day of week 1 | — |
| `5.5204` | Pump day of week 2 | — |
| `5.5205` | Pump day of week 3 | — |
| `5.5206` | Pump day of week 4 | — |
| `5.5207` | Pump day of week 5 | — |
| `5.5208` | Pump day of week 6 | — |
| `5.5319` | Out1 day of week 4 | — |
| `5.5320` | Out1 day of week 5 | — |
| `5.5321` | Out1 day of week 6 | — |
| `5.5332` | Out2 day of week 4 | — |
| `5.5333` | Out2 day of week 5 | — |
| `5.5334` | Out2 day of week 6 | — |
| `5.5358` | Out4 day of week 4 | — |
| `5.5359` | Out4 day of week 5 | — |
| `5.5360` | Out4 day of week 6 | — |
| `5.5501` | Out5 day of week 1 | — |
| `5.5502` | Out5 day of week 2 | — |
| `5.5503` | Out5 day of week 3 | — |
| `5.5504` | Out5 day of week 4 | — |
| `5.5505` | Out5 day of week 5 | — |
| `5.5506` | Out5 day of week 6 | — |
| `5.5535` | Out6 day of week 1 | — |
| `5.5536` | Out6 day of week 2 | — |
| `5.5537` | Out6 day of week 3 | — |
| `5.5538` | Out6 day of week 4 | — |
| `5.5539` | Out6 day of week 5 | — |
| `5.5540` | Out6 day of week 6 | — |
| `5.5569` | Out7 day of week 1 | — |
| `5.5570` | Out7 day of week 2 | — |
| `5.5571` | Out7 day of week 3 | — |
| `5.5572` | Out7 day of week 4 | — |
| `5.5573` | Out7 day of week 5 | — |
| `5.5574` | Out7 day of week 6 | — |
| `5.5603` | Out8 day of week 1 | — |
| `5.5604` | Out8 day of week 2 | — |
| `5.5605` | Out8 day of week 3 | — |
| `5.5606` | Out8 day of week 4 | — |
| `5.5607` | Out8 day of week 5 | — |
| `5.5608` | Out8 day of week 6 | — |
| `5.5637` | Out9 day of week 1 | — |
| `5.5638` | Out9 day of week 2 | — |
| `5.5639` | Out9 day of week 3 | — |
| `5.5640` | Out9 day of week 4 | — |
| `5.5641` | Out9 day of week 5 | — |
| `5.5642` | Out9 day of week 6 | — |
| `5.5671` | Out10 day of week 1 | — |
| `5.5672` | Out10 day of week 2 | — |
| `5.5673` | Out10 day of week 3 | — |
| `5.5674` | Out10 day of week 4 | — |
| `5.5675` | Out10 day of week 5 | — |
| `5.5676` | Out10 day of week 6 | — |
| `5.22260` | Out1 t1 active | — |
| `5.22261` | Out1 t2 active | — |
| `5.22262` | Out1 t3 active | — |
| `5.22263` | Out1 t4 active | — |
| `5.22264` | Out1 t5 active | — |
| `5.22265` | Out1 t6 active | — |
| `5.22266` | Out2 t1 active | — |
| `5.22267` | Out2 t2 active | — |
| `5.22268` | Out2 t3 active | — |
| `5.22269` | Out2 t4 active | — |
| `5.22270` | Out2 t5 active | — |
| `5.22271` | Out2 t6 active | — |
| `5.22278` | Out4 t1 active | — |
| `5.22279` | Out4 t2 active | — |
| `5.22280` | Out4 t3 active | — |
| `5.22281` | Out4 t4 active | — |
| `5.22282` | Out4 t5 active | — |
| `5.22283` | Out4 t6 active | — |
| `5.22284` | Out5 t1 active | — |
| `5.22285` | Out5 t2 active | — |
| `5.22286` | Out5 t3 active | — |
| `5.22287` | Out5 t4 active | — |
| `5.22288` | Out5 t5 active | — |
| `5.22289` | Out5 t6 active | — |
| `5.22290` | Out6 t1 active | — |
| `5.22291` | Out6 t2 active | — |
| `5.22292` | Out6 t3 active | — |
| `5.22293` | Out6 t4 active | — |
| `5.22294` | Out6 t5 active | — |
| `5.22295` | Out6 t6 active | — |
| `5.22296` | Out7 t1 active | — |
| `5.22297` | Out7 t2 active | — |
| `5.22298` | Out7 t3 active | — |
| `5.22299` | Out7 t4 active | — |
| `5.22300` | Out7 t5 active | — |
| `5.22301` | Out7 t6 active | — |
| `5.22302` | Out8 t1 active | — |
| `5.22303` | Out8 t2 active | — |
| `5.22304` | Out8 t3 active | — |
| `5.22305` | Out8 t4 active | — |
| `5.22306` | Out8 t5 active | — |
| `5.22307` | Out8 t6 active | — |
| `5.22308` | Out9 t1 active | — |
| `5.22309` | Out9 t2 active | — |
| `5.22310` | Out9 t3 active | — |
| `5.22311` | Out9 t4 active | — |
| `5.22312` | Out9 t5 active | — |
| `5.22313` | Out9 t6 active | — |
| `5.22314` | Out10 t1 active | — |
| `5.22315` | Out10 t2 active | — |
| `5.22316` | Out10 t3 active | — |
| `5.22317` | Out10 t4 active | — |
| `5.22318` | Out10 t5 active | — |
| `5.22319` | Out10 t6 active | — |
| `5.22320` | Pump t1 active | — |
| `5.22321` | Pump t2 active | — |
| `5.22322` | Pump t3 active | — |
| `5.22323` | Pump t4 active | — |
| `5.22324` | Pump t5 active | — |
| `5.22325` | Pump t6 active | — |

</details>

## 3. Special topics

| MQTT ID | Description | Payload | Entity in HA |
| --- | --- | --- | --- |
| `10` | Current message list of the PoolAccess app (Automatic devices) | list of message codes (`8.5` to `8.47`) | Messages (`sensor`) plus `bayrol_message` events |
| `8.2002` | Device alarm state (PM5 only) | dict: `active`, `quit_required`, `is_quit`, `module` (no `v` key) | Device Alarm (`binary_sensor`) |
| `8.2003` | Device info state (PM5 only) | dict, same shape as `8.2002` | Device Info (`binary_sensor`) |
