
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

# Function to callback when the client connects to the MQTT broker
def broker_connected(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    # Subscribe to the MQTT topic that controls the LED
    client.subscribe("LED")

# Function to callback when a message is received from the MQTT broker
def message_recieved(client, userdata, msg):
    # Turns the LED on if the message recieved is '1'
    if msg.payload.decode() == "1":
        GPIO.output(18, GPIO.HIGH)
    # Turn the LED off if the message recieved is '0'
    elif msg.payload.decode() == "0":
        GPIO.output(18, GPIO.LOW)

# Setup in BCM mode for Raspberry Pi GPIO
GPIO.setmode(GPIO.BCM)

# GPIO pin 18 (GPIO 24) as an output for the LED
GPIO.setup(18, GPIO.OUT)

# MQTT client instance
client = mqtt.Client()

# Callback functions to the MQTT client
client.on_connect = broker_connected
client.on_message = message_recieved

# Connection to the MQTT broker
client.connect("localhost", 1883, 60)

# Initiate meesage loop
client.loop_forever()
