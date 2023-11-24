
import json
import paho.mqtt.client as mqtt

# Configuration data loaded from the JSON file
with open('config.json', 'r') as file:
    config = json.load(file)

# A function to assess the conditions specified in the config.json file
def condition_value(condition, message):
    # Compares and checks if the condition is greater than
    if condition['compare'] == '>':
        return float(message) > condition['value']
    # Compares and checks if the condition is less than or equal to
    elif condition['compare'] == '<=':
        return float(message) <= condition['value']
    return False

# Triggered upon the client's connection to the MQTT broker
def broker_connected(client, userdata, flags, rc):
    # Prints a message when client is connected to MQTT broker
    print("Connected"+str(rc))
    # Will subscribe to MQTT topics based on the conditions implemented in the JSON config file
    for item in config:
        for condition in item['conditions']:
            client.subscribe(condition['topic'])

# Triggered upon receiving a message from the MQTT broker
def message_received(client, userdata, msg):
    # Prints message when the message is received
    print("Recieved: '" + str(msg.payload.decode()) + "' on topic: '> 
    for item in config:
        for condition in item['conditions']:
            # If the topic is the same, it will check the condition
            if msg.topic == condition['topic']:
                if evaluate_condition(condition, msg.payload.decode()):
                    # If condition is good and matches it will publish the result
                    for result in item['results']:
                        client.publish(result['topic'], result['value'])

# Defining functions for possible callback
client.broker_connected = broker_connected
client.message_received = message_received

# Structure, setup of MQTT client defining funcitons for callback
client = mqtt.Client()

# Connection to the MQTT broker
client.connect("localhost", 1883, 60)

# Initiate network loop
client.loop_forever()