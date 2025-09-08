[![Static Badge](https://img.shields.io/badge/HACS-Custom-41BDF5?style=for-the-badge&logo=homeassistantcommunitystore&logoColor=white)](https://github.com/hacs/integration) 
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/0xQuantumHome/bayrol-home-hassistant?style=for-the-badge) 
![GitHub Release Date](https://img.shields.io/github/release-date/0xQuantumHome/bayrol-home-hassistant?style=for-the-badge&label=Latest%20Release) [![GitHub Release](https://img.shields.io/github/v/release/0xQuantumHome/bayrol-home-hassistant?style=for-the-badge)](https://github.com/0xQuantumHome/bayrol-home-hassistant/releases)


# Bayrol Pool Access Integration for Home Assistant

This custom integration allows you to monitor your Bayrol Pool Access device in Home Assistant. It uses a direct MQTT connection to the Bayrol Cloud.

## Features

- 40+ entities (including pH, Redox, Salt levels, alarm levels, etc.)
- Real-time updates via MQTT connection

## Tested Devices

- Bayrol Automatic Salt 5 (AS5)
- Bayrol Automatic Cl-pH
- Pool Manager 5 Chlorine

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


