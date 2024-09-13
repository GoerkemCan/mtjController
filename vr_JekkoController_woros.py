import numpy as np
import paho.mqtt.client as mqtt
import json

class InputActionClient:

    def __init__(self) -> None:
        # Initialize the MQTT client
        self.mqtt_client = mqtt.Client()

        # Set up MQTT callbacks
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message

        # Connect to the MQTT broker
        self.mqtt_client.connect("master.local", 1883, 60)

        # Subscribe to relevant topics (adapt topic names based on your setup)
        self.mqtt_client.subscribe("unity/joystick")
        self.mqtt_client.subscribe("unity/buttons")

        # Start the MQTT loop
        self.mqtt_client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected to MQTT Broker with result code {rc}")

    def on_message(self, client, userdata, msg):
        # Handle incoming MQTT messages and map them to joystick or button actions
        topic = msg.topic
        payload = msg.payload.decode('utf-8')

        if topic == "unity/joystick":
            self.handle_joystick_message(payload)
        elif topic == "unity/buttons":
            self.handle_button_message(payload)

    def handle_joystick_message(self, payload):
        # Assume payload is in JSON format: {"inputName": "Left Thumbstick", "value": [x, y]}
        data = json.loads(payload)

        joystick_name = data['inputName']
        joystick_value = data['value']

        # Map the joystick input to print axis values for now
        if joystick_name == "Left Thumbstick":
            abs_x = np.clip(joystick_value[0], -1.0, 1.0)
            abs_y = np.clip(joystick_value[1], -1.0, 1.0)
            print(f"Left Thumbstick X: {abs_x}, Y: {abs_y}")
        elif joystick_name == "Right Thumbstick":
            abs_rx = np.clip(joystick_value[0], -1.0, 1.0)
            abs_ry = np.clip(joystick_value[1], -1.0, 1.0)
            print(f"Right Thumbstick X: {abs_rx}, Y: {abs_ry}")

    def handle_button_message(self, payload):
        # Assume payload is in JSON format: {"inputName": "A", "value": 1}
        data = json.loads(payload)

        button_name = data['inputName']
        button_state = data['value']

        # Map button inputs to print statements for now
        match button_name:
            case "Right A Button":
                print(f"Button A: {button_state}")
            case "Right B Button":
                print(f"Button B: {button_state}")
            case "Left Index Trigger":
                print(f"Left Index Trigger: {button_state}")
            case "Left Hand Trigger":
                print(f"Left Hand Trigger: {button_state}")
            # Add additional button mappings as needed

def main() -> None:
    joystick_client = InputActionClient()

    try:
        # Keep the script running to process MQTT messages
        input("Press Enter to exit...\n")
    except KeyboardInterrupt:
        print("Shutting down...")

if __name__ == "__main__":
    main()
