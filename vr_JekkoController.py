import numpy as np
import rclpy
import os

from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle

#from jekko_interfaces.action import JoystickInterface

import paho.mqtt.client as mqtt

class InputActionClient(Node):

    def __init__(self) -> None:

        super().__init__("joystick_action_client")

        #self.__input_client = ActionClient(self, JoystickInterface, "input_interface")

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

        self.__goal = JoystickInterface.Goal()

        self.mqtt_client.loop_start()

       def on_connect(self, client, userdata, flags, rc):
        self.get_logger().info(f"Connected to MQTT Broker with result code {rc}")

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
        import json
        data = json.loads(payload)

        joystick_name = data['inputName']
        joystick_value = data['value']

        # Map the joystick input to the corresponding axis values
        if joystick_name == "Left Thumbstick":
            self.__goal.abs_x = np.clip(joystick_value[0], -1.0, 1.0)
            self.__goal.abs_y = np.clip(joystick_value[1], -1.0, 1.0)
        elif joystick_name == "Right Thumbstick":
            self.__goal.abs_rx = np.clip(joystick_value[0], -1.0, 1.0)
            self.__goal.abs_ry = np.clip(joystick_value[1], -1.0, 1.0)

        # Send the updated goal asynchronously
        #self.__input_client.wait_for_server()
        #self.__input_client.send_goal_async(self.__goal)

    def handle_button_message(self, payload):
        # Assume payload is in JSON format: {"inputName": "A", "value": 1}
        import json
        data = json.loads(payload)

        button_name = data['inputName']
        button_state = data['value']

        # Map button inputs to the corresponding goal fields
        match button_name:
            case "A":
                self.__goal.btn_a = button_state
            case "B":
                self.__goal.btn_b = button_state
            case "Left Index Trigger":
                self.__goal.btn_l = button_state
            case "Left Hand Trigger":
                self.__goal.btn_r = button_state
            # Add additional button mappings as needed

        # Send the updated goal asynchronously
        #self.__input_client.wait_for_server()
        #self.__input_client.send_goal_async(self.__goal)

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().warning(f"ACK: {feedback}")

def main(args=None) -> None:
    rclpy.init(args=args)

    joystick_client = InputActionClient()

    try:
        rclpy.spin(joystick_client)
    except KeyboardInterrupt:
        joystick_client.destroy_node()
        rclpy.shutdown()

    exit()

if __name__ == "__main__":
    main()