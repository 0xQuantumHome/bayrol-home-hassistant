#!/usr/bin/env python3
"""
MQTT Topic Sniffer for Bayrol Pool Devices

This script discovers ALL MQTT topics that a Bayrol device sends,
including topics not defined in const.py (like Flow, Filterpump, etc.)

Usage:
    python scripts/mqtt_sniffer.py --device-id YOUR_DEVICE_SERIAL --token YOUR_ACCESS_TOKEN

    Or use environment variables:
    BAYROL_DEVICE_ID=xxx BAYROL_ACCESS_TOKEN=xxx python scripts/mqtt_sniffer.py

The script will:
1. Connect to Bayrol MQTT broker
2. Subscribe to ALL topics for your device using wildcard
3. Log every discovered topic with its value
4. Save results to a JSON file for analysis
"""

import argparse
import json
import logging
import os
import signal
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

import paho.mqtt.client as mqtt

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Bayrol MQTT defaults (can be overridden via --host / --port)
BAYROL_HOST = os.environ.get("BAYROL_MQTT_HOST", "www.bayrol-poolaccess.de")
BAYROL_PORT = int(os.environ.get("BAYROL_MQTT_PORT", "8083"))

# Known topics from const.py (for comparison)
KNOWN_TOPICS_AUTOMATIC = {
    "4.2",
    "4.3",
    "4.4",
    "4.5",
    "4.7",
    "4.26",
    "4.27",
    "4.28",
    "4.34",
    "4.37",
    "4.38",
    "4.47",
    "4.67",
    "4.68",
    "4.69",
    "4.82",
    "4.89",
    "4.98",
    "4.102",
    "4.107",
    "4.182",
    "5.3",
    "5.80",
    "5.98",
}

KNOWN_TOPICS_AUTOMATIC_SALT = KNOWN_TOPICS_AUTOMATIC | {
    "4.51",
    "4.66",
    "4.91",
    "4.100",
    "4.104",
    "4.105",
    "4.112",
    "4.119",
    "4.144",
    "5.40",
    "5.41",
}

KNOWN_TOPICS_AUTOMATIC_CL_PH = KNOWN_TOPICS_AUTOMATIC | {"4.90", "5.175", "5.169"}

KNOWN_TOPICS_PM5 = {
    "4.3001",
    "4.3002",
    "4.3003",
    "4.3049",
    "4.3051",
    "4.3053",
    "4.4001",
    "4.4022",
    "4.4033",
    "4.4069",
    "4.4132",
    "5.5433",
    "5.5434",
    "5.5435",
    "5.5436",
    "5.6012",
    "5.6015",
    "5.6064",
    "5.6065",
    "5.6068",
    "5.6069",
}

ALL_KNOWN_TOPICS = (
    KNOWN_TOPICS_AUTOMATIC_SALT | KNOWN_TOPICS_AUTOMATIC_CL_PH | KNOWN_TOPICS_PM5
)


class MQTTSniffer:
    """Sniffs all MQTT topics from a Bayrol device."""

    def __init__(
        self, device_id: str, access_token: str, output_dir: str = "discovered_topics"
    ):
        self.device_id = device_id
        self.access_token = access_token
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        self.client: Optional[mqtt.Client] = None
        self.discovered_topics: Dict[str, Dict[str, Any]] = {}
        self.new_topics: Dict[str, Dict[str, Any]] = {}  # Topics not in const.py
        self.previously_discovered: set = set()  # Topics from previous runs
        self.start_time = datetime.now()
        self.message_count = 0
        self.running = True

        # Load previously discovered topics
        self._load_previous_discoveries()

    def _load_previous_discoveries(self):
        """Load topics from previous discovery sessions."""
        # Look for existing discovery files for this device
        pattern = f"all_topics_{self.device_id}_*.json"
        existing_files = sorted(self.output_dir.glob(pattern), reverse=True)

        if existing_files:
            # Load the most recent file
            latest_file = existing_files[0]
            try:
                with open(latest_file, "r") as f:
                    data = json.load(f)
                    topics = data.get("topics", {})
                    self.previously_discovered = set(topics.keys())
                    logger.info(
                        f"Loaded {len(self.previously_discovered)} previously discovered topics from {latest_file.name}"
                    )
            except Exception as e:
                logger.warning(f"Could not load previous discoveries: {e}")

        # Also check for a persistent "known topics" file
        persistent_file = self.output_dir / f"known_topics_{self.device_id}.json"
        if persistent_file.exists():
            try:
                with open(persistent_file, "r") as f:
                    data = json.load(f)
                    self.previously_discovered.update(data.get("topics", []))
                    logger.info(
                        f"Loaded persistent known topics from {persistent_file.name}"
                    )
            except Exception as e:
                logger.warning(f"Could not load persistent file: {e}")

    def _save_persistent_topics(self):
        """Save all discovered topics to a persistent file."""
        persistent_file = self.output_dir / f"known_topics_{self.device_id}.json"
        all_topics = self.previously_discovered | set(self.discovered_topics.keys())

        with open(persistent_file, "w") as f:
            json.dump(
                {
                    "device_id": self.device_id,
                    "last_updated": datetime.now().isoformat(),
                    "topics": sorted(list(all_topics)),
                },
                f,
                indent=2,
            )
        logger.info(f"Saved {len(all_topics)} topics to {persistent_file}")

    def on_connect(self, client, userdata, flags, rc):
        """Handle connection to MQTT broker."""
        if rc == 0:
            logger.info(f"Connected to Bayrol MQTT broker")
            logger.info(f"Device ID: {self.device_id}")

            # Subscribe to ALL topics for this device using wildcard
            wildcard_topic = f"d02/{self.device_id}/v/#"
            client.subscribe(wildcard_topic)
            logger.info(f"Subscribed to: {wildcard_topic}")
            logger.info("-" * 60)
            logger.info("Waiting for messages... (Press Ctrl+C to stop)")
            logger.info("-" * 60)
        else:
            logger.error(f"Connection failed with code: {rc}")
            if rc == 5:
                logger.error("Authentication failed - check your access token")
            self.running = False

    def on_message(self, client, userdata, msg):
        """Handle incoming MQTT message."""
        self.message_count += 1

        # Parse topic
        topic_parts = msg.topic.split("/")
        sensor_id = topic_parts[-1] if len(topic_parts) > 0 else "unknown"

        # Store raw payload
        raw_payload = msg.payload.decode("utf-8", errors="replace")

        # Parse payload
        try:
            payload = json.loads(msg.payload)
            # Handle different payload formats:
            # - Dict with "v" key: {"v": 123}
            # - List: [1, 2, 3]
            # - Direct value: 123
            if isinstance(payload, dict):
                value = payload.get("v", payload)
            else:
                # Lists, numbers, strings, etc.
                value = payload
        except json.JSONDecodeError:
            value = raw_payload
            payload = raw_payload

        timestamp = datetime.now().isoformat()

        # Check if this is a new topic
        is_new_this_session = sensor_id not in self.discovered_topics
        is_new_ever = (
            sensor_id not in self.previously_discovered and is_new_this_session
        )
        is_unknown = sensor_id not in ALL_KNOWN_TOPICS

        # Check if this is a new/different value for a known topic
        is_new_value = False
        if not is_new_this_session and is_unknown:
            existing = self.discovered_topics[sensor_id]
            value_str = json.dumps(value) if isinstance(value, (list, dict)) else value
            sample_strs = [
                json.dumps(v) if isinstance(v, (list, dict)) else v
                for v in existing.get("sample_values", [])
            ]
            is_new_value = value_str not in sample_strs

        # Store topic info
        topic_info = {
            "sensor_id": sensor_id,
            "full_topic": msg.topic,
            "raw_payload": raw_payload,
            "parsed_payload": payload,
            "value": value,
            "value_type": type(value).__name__,
            "first_seen": timestamp
            if is_new_this_session
            else self.discovered_topics.get(sensor_id, {}).get("first_seen", timestamp),
            "last_seen": timestamp,
            "update_count": self.discovered_topics.get(sensor_id, {}).get(
                "update_count", 0
            )
            + 1,
            "is_in_const_py": not is_unknown,
            "sample_values": self.discovered_topics.get(sensor_id, {}).get(
                "sample_values", []
            ),
            "raw_samples": self.discovered_topics.get(sensor_id, {}).get(
                "raw_samples", []
            ),
        }

        # Store sample values (up to 10 unique values)
        # Convert to string for comparison since lists aren't hashable
        value_str = json.dumps(value) if isinstance(value, (list, dict)) else value
        sample_strs = [
            json.dumps(v) if isinstance(v, (list, dict)) else v
            for v in topic_info["sample_values"]
        ]
        if value_str not in sample_strs and len(topic_info["sample_values"]) < 10:
            topic_info["sample_values"].append(value)
            topic_info["raw_samples"].append(raw_payload)

        self.discovered_topics[sensor_id] = topic_info

        # Track unknown topics separately
        if is_unknown:
            self.new_topics[sensor_id] = topic_info

        # Log the message
        if is_new_ever:
            status = "NEW!   "
        elif is_new_this_session:
            status = "SEEN   "  # Known from previous runs
        elif is_new_value:
            status = "UPDATE "  # New value for known topic
        else:
            status = "       "

        unknown_marker = " [NOT IN CONST.PY]" if is_unknown else ""

        # Try to guess coefficient for numeric values
        coefficient_hint = ""
        if isinstance(value, (int, float)) and value != 0:
            # Common coefficients: 10, 100, 1000
            if abs(value) > 100:
                coefficient_hint = (
                    f" (maybe /10={value / 10:.1f} or /100={value / 100:.2f})"
                )

        if is_new_ever or (is_new_this_session and is_unknown):
            logger.info(
                f"{status} Topic: {sensor_id:12} | Value: {str(value):15}{coefficient_hint}{unknown_marker}"
            )
            logger.info(f"         RAW: {raw_payload}")
            logger.info(f"         Full topic: {msg.topic}")
            logger.info("-" * 80)
        elif is_new_value:
            # New value discovered for existing topic!
            old_values = self.discovered_topics[sensor_id].get("sample_values", [])
            logger.info(
                f"{status} Topic: {sensor_id:12} | Value: {str(value):15}{coefficient_hint}{unknown_marker}"
            )
            logger.info(f"         Previous values: {old_values[:5]}")
            logger.info(f"         RAW: {raw_payload}")
            logger.info("-" * 80)
        elif is_unknown:
            # Unknown but seen before - still show updates
            logger.info(
                f"{status} Topic: {sensor_id:12} | Value: {str(value):15}{coefficient_hint}{unknown_marker}"
            )
        else:
            logger.debug(f"{status} Topic: {sensor_id:12} | Value: {str(value):15}")

    def on_disconnect(self, client, userdata, rc):
        """Handle disconnection from MQTT broker."""
        if rc != 0:
            logger.warning(f"Unexpected disconnection (code: {rc})")
        else:
            logger.info("Disconnected from broker")

    def start(self):
        """Start the MQTT sniffer."""
        logger.info("=" * 60)
        logger.info("BAYROL MQTT TOPIC SNIFFER")
        logger.info("=" * 60)

        # Create MQTT client
        self.client = mqtt.Client(transport="websockets")
        self.client.username_pw_set(self.access_token, "1")
        self.client.tls_set()

        # Set callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect

        # Connect
        try:
            logger.info(f"Connecting to {BAYROL_HOST}:{BAYROL_PORT}...")
            self.client.connect(BAYROL_HOST, BAYROL_PORT, keepalive=60)
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return

        # Start loop
        self.client.loop_start()

        # Wait for messages
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("\nStopping sniffer...")

        self.stop()

    def stop(self):
        """Stop the sniffer and save results."""
        self.running = False

        if self.client:
            self.client.loop_stop()
            self.client.disconnect()

        # Save results
        self.save_results()

    def save_results(self):
        """Save discovered topics to files."""
        duration = (datetime.now() - self.start_time).total_seconds()

        # Summary
        logger.info("")
        logger.info("=" * 60)
        logger.info("DISCOVERY RESULTS")
        logger.info("=" * 60)
        logger.info(f"Duration: {duration:.1f} seconds")
        logger.info(f"Total messages received: {self.message_count}")
        logger.info(f"Unique topics discovered: {len(self.discovered_topics)}")
        logger.info(f"NEW topics (not in const.py): {len(self.new_topics)}")

        if self.new_topics:
            logger.info("")
            logger.info("NEW TOPICS FOUND:")
            logger.info("-" * 60)
            for sensor_id, info in sorted(self.new_topics.items()):
                logger.info(f"  {sensor_id:12} | Samples: {info['sample_values'][:3]}")

        # Save all discovered topics
        all_topics_file = (
            self.output_dir
            / f"all_topics_{self.device_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(all_topics_file, "w") as f:
            json.dump(
                {
                    "device_id": self.device_id,
                    "discovery_time": self.start_time.isoformat(),
                    "duration_seconds": duration,
                    "message_count": self.message_count,
                    "topics": self.discovered_topics,
                },
                f,
                indent=2,
                default=str,
            )
        logger.info(f"\nAll topics saved to: {all_topics_file}")

        # Save new topics separately
        if self.new_topics:
            new_topics_file = (
                self.output_dir
                / f"new_topics_{self.device_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            with open(new_topics_file, "w") as f:
                json.dump(
                    {
                        "device_id": self.device_id,
                        "discovery_time": self.start_time.isoformat(),
                        "new_topics": self.new_topics,
                    },
                    f,
                    indent=2,
                    default=str,
                )
            logger.info(f"New topics saved to: {new_topics_file}")

            # Generate const.py snippet
            self.generate_const_snippet()

        # Save persistent topics file (for future runs)
        self._save_persistent_topics()

    def generate_const_snippet(self):
        """Generate a code snippet to add to const.py."""
        if not self.new_topics:
            return

        snippet_file = self.output_dir / f"const_snippet_{self.device_id}.py"

        lines = [
            "# NEW DISCOVERED TOPICS",
            f"# Discovered from device: {self.device_id}",
            f"# Discovery date: {datetime.now().isoformat()}",
            "#",
            "# Add these to the appropriate SENSOR_TYPES_* dictionary in const.py",
            "# You may need to determine the correct coefficient and unit for each sensor",
            "",
            "NEW_DISCOVERED_SENSORS = {",
        ]

        for sensor_id, info in sorted(self.new_topics.items()):
            sample_value = (
                info["sample_values"][0] if info["sample_values"] else "unknown"
            )
            value_type = info["value_type"]

            # Try to guess the sensor type
            coefficient = "1"
            unit = "None"
            name = f"Unknown Sensor {sensor_id}"

            # Guess based on value patterns
            if isinstance(sample_value, (int, float)):
                if sample_value > 1000:
                    coefficient = "1"
                    unit = '"mV"'  # Likely voltage
                elif 0 < sample_value < 20:
                    coefficient = "10"
                    unit = "None"  # Likely pH or similar
                elif 0 < sample_value < 100:
                    coefficient = "1"
                    unit = '"%"'  # Likely percentage

            lines.extend(
                [
                    f'    "{sensor_id}": {{',
                    f'        "name": "{name}",  # TODO: Determine actual name',
                    f'        "device_class": None,',
                    f'        "state_class": SensorStateClass.MEASUREMENT,',
                    f'        "coefficient": {coefficient},  # TODO: Verify coefficient',
                    f'        "unit_of_measurement": {unit},  # TODO: Verify unit',
                    f'        "entity_type": "sensor",',
                    f"        # Sample values: {info['sample_values'][:5]}",
                    f"    }},",
                ]
            )

        lines.append("}")

        with open(snippet_file, "w") as f:
            f.write("\n".join(lines))

        logger.info(f"Code snippet saved to: {snippet_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Sniff all MQTT topics from a Bayrol pool device"
    )
    parser.add_argument(
        "--device-id",
        default=os.environ.get("BAYROL_DEVICE_ID"),
        help="Device serial number (or set BAYROL_DEVICE_ID env var)",
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("BAYROL_ACCESS_TOKEN"),
        help="Access token (or set BAYROL_ACCESS_TOKEN env var)",
    )
    parser.add_argument(
        "--host",
        default=BAYROL_HOST,
        help="MQTT broker host (default: www.bayrol-poolaccess.de, or BAYROL_MQTT_HOST env)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=BAYROL_PORT,
        help="MQTT broker port (default: 8083, or BAYROL_MQTT_PORT env)",
    )
    parser.add_argument(
        "--output-dir",
        default="discovered_topics",
        help="Directory to save results (default: discovered_topics)",
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=0,
        help="Run for N seconds then stop (0 = run until Ctrl+C)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show all messages, not just new ones",
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("BAYROL_ACCESS_TOKEN"),
        help="Access token (or set BAYROL_ACCESS_TOKEN env var)",
    )
    parser.add_argument(
        "--output-dir",
        default="discovered_topics",
        help="Directory to save results (default: discovered_topics)",
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=0,
        help="Run for N seconds then stop (0 = run until Ctrl+C)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show all messages, not just new ones",
    )

    args = parser.parse_args()

    if not args.device_id:
        logger.error("Device ID required! Use --device-id or set BAYROL_DEVICE_ID")
        logger.info("")
        logger.info("How to get your device ID and token:")
        logger.info("  Use the Bayrol app link code flow:")
        logger.info(
            "  GET https://www.bayrol-poolaccess.de/webapi/p/v3/getaccesstoken?code=XXXXXXXX"
        )
        logger.info("  Response contains 'deviceSerial' (device ID) and 'accessToken'")
        sys.exit(1)

    if not args.token:
        logger.error("Access token required! Use --token or set BAYROL_ACCESS_TOKEN")
        sys.exit(1)

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Allow overriding host/port at runtime
    global BAYROL_HOST, BAYROL_PORT
    BAYROL_HOST = args.host
    BAYROL_PORT = args.port

    sniffer = MQTTSniffer(
        device_id=args.device_id, access_token=args.token, output_dir=args.output_dir
    )

    # Handle duration
    if args.duration > 0:

        def stop_after_duration():
            time.sleep(args.duration)
            logger.info(f"\nDuration of {args.duration}s reached, stopping...")
            sniffer.running = False

        import threading

        timer = threading.Thread(target=stop_after_duration, daemon=True)
        timer.start()

    # Handle signals
    def signal_handler(sig, frame):
        logger.info("\nReceived stop signal...")
        sniffer.running = False

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start sniffing
    sniffer.start()


if __name__ == "__main__":
    main()
