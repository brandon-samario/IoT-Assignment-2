
#include <WiFi.h>
#include <PubSubClient.h>

// WiFi settings
const char* ssid = "WiFi name";  // WiFi SSID name of network
const char* password = "WiFi password";  // WiFi password

// MQTT broker settings
const char* mqtt_server = "10.0.0.21";  // Set IP address of Raspberry Pi running the MQTT broker
const int mqtt_port = 1883;  // Default MQTT port 

// ESP32 client settings
WiFiClient espClient;
PubSubClient client(espClient);

// Setting the initiation of the WiFi and MQTT server & port
void setup() {
    Serial.begin(115200);  // Start serial communication baud rate at 115200 
    initiate_wifi();  // Connect to WiFi
    client.setServer(mqtt_server, mqtt_port);  // Set the MQTT server and port
}

// Function to connect to the WiFi network
void initiate_wifi() {
    WiFi.begin(ssid, password);  // Start WiFi connectivity
    while (WiFi.status() != WL_CONNECTED) {  // Wait for status of Wi-Fi until it is connected 
    delay(1000); // Wait time of 1 second
	Serial.println("WiFi connected");  // Print command, message once WiFi is connected
}

// Loop to read the potentiometer and publish the value to an MQTT topic
void loop() {
    if (!client.connected()) { // Client is connected
        reconnect();  // Attempt of reconnection to the MQTT broker if disconnected
    }
    client.loop();  // Keep connection of MQTT
    
    // Reads the analog signal from the potentiometer connected to the pin 34
    int potvalue = analogRead(34);
    // Read the value on potentiometer (0 to 100)
    int mapvalue = map(potvalue, 0, 4095, 0, 100);

    // Publish the mapped value to the MQTT topic
    char message[50];
    sprintf(message, "%d", mapvalue);
    client.publish("potentiometer", message);
    Serial.println(message);  // Print command, a message to the serial monitor for debugging
    delay(1000);  // Wait time of 1 second
}

// Function if disconnected it will reconnect to the MQTT broker 
void reconnect() {
    while (!client.connected()) {
        if (client.connect("ESP32 client")) {
            // Nothing needs to be done, if the client is already connected
        } else {
            delay(5000);  // Wait 5 seconds before reattempting
        }
    }
}
