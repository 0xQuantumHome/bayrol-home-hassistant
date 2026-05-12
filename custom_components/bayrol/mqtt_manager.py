"""MQTT Manager for Bayrol integration."""

from __future__ import annotations

import logging
import threading
import paho.mqtt.client as paho
import json

from homeassistant.core import HomeAssistant

from .const import (
    BAYROL_HOST,
    BAYROL_PORT,
)

_LOGGER = logging.getLogger(__name__)


class BayrolMQTTManager:
    """Manage the Bayrol MQTT connection."""

    def __init__(self, hass: HomeAssistant, device_id: str, mqtt_user: str):
        """Initialize the Bayrol MQTT manager."""
        self.hass = hass
        self.mqtt_user = mqtt_user
        self.device_id = device_id
        self.client = None
        self.thread = None
        self._subscribers = {}

    def subscribe(self, topic: str, callback):
        """Subscribe to a topic with a callback."""
        self._subscribers[topic] = callback
        if self.client and self.client.is_connected():
            self.client.subscribe(f"d02/{self.device_id}/v/{topic}")
            # Push to receive initial value
            self.client.publish(f"d02/{self.device_id}/g/{topic}")

    def _on_connect(self, client, userdata, flags, rc):
        """Handle the connection to the MQTT broker."""
        if rc == 0:
            _LOGGER.info("Connected to Bayrol MQTT broker with result code 0 (Success)")
            # Resubscribe to all topics
            for topic in self._subscribers:
                client.subscribe(f"d02/{self.device_id}/v/{topic}")
                client.publish(f"d02/{self.device_id}/g/{topic}")
        else:
            _LOGGER.debug("Failed to connect to MQTT broker, result code: %s", rc)

    def _on_message(self, client, userdata, msg):
        """Handle the incoming messages from the MQTT broker."""
        _LOGGER.debug("Received message from topic: %s", msg.topic)

        # Just get the last part of the topic
        topic_parts = msg.topic.split("/")
        topic = topic_parts[-1]

        if topic in self._subscribers:
            try:
                parsed = json.loads(msg.payload)
                # Most topics use {"v": value}. Alarm topics (8.2002, 8.2003)
                # use a richer dict without a "v" key — pass the full dict so
                # subscribers can read quit_required, active, module, etc.
                value = parsed.get("v", parsed)
                callback = self._subscribers[topic]
                self.hass.loop.call_soon_threadsafe(lambda cb=callback, v=value: cb(v))
            except Exception as e:
                _LOGGER.error("Invalid payload for %s: %s", msg.topic, e)
        else:
            _LOGGER.warning("Received message for unknown topic: %s", msg.topic)

    def _start(self):
        """Start the MQTT manager."""
        self.client = paho.Client(transport="websockets")
        self.client.username_pw_set(self.mqtt_user, "1")
        self.client.tls_set()
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        try:
            self.client.connect(BAYROL_HOST, BAYROL_PORT, 60)
            _LOGGER.debug("MQTT connect() called for %s:%s", BAYROL_HOST, BAYROL_PORT)
        except Exception as e:
            _LOGGER.error("MQTT connect() failed: %s", e)
        self.client.loop_forever()

    def start(self):
        """Start the MQTT manager."""
        _LOGGER.debug("Starting MQTT manager")
        if not self.thread:
            self.thread = threading.Thread(target=self._start, daemon=True)
            self.thread.start()
