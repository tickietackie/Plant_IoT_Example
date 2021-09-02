#include <ESP8266WiFi.h>  // included in standard library 
#include <PubSubClient.h> // Install PubSubClient via Library Manager 
#include <DHT.h> // Install DHT Sensor Library via Library Manager 
#include <ArduinoJson.h> // Install ArduinoJson via Library Manager 
#include <NTPClient.h> // Install NTPClient Library via Library Manager 
#include <WifiUdp.h> // included in standard library 

// Network Time Protocol (NTP): Settings for getting Timestamps
// Note: ESP8266 does not have a battery-powered clock, so we need to fetch the current 
// time from NTP time servers on the internet
#define NTP_OFFSET   2 * 60 * 60      // In seconds (2 hours, Timezone: UTC+2 (Berlin))
#define NTP_INTERVAL 60 * 1000    // In milliseconds (Update-Interval 1 Minute) 
#define NTP_ADDRESS  "europe.pool.ntp.org" // NTP Server Pool for Europe
WiFiUDP ntpUDP; 
NTPClient timeClient(ntpUDP, NTP_ADDRESS, NTP_OFFSET, NTP_INTERVAL); // The NTP Client

// DHT Sensor (Reference-Architecture from lecture)
#define DHTTYPE DHT11 // may be DHT11 or DHT22 
uint8_t DHTPin = D1;  // DHT11-Sensor connected to Pin D1 (VCC should be connected to 3,3V, GRN to GRN)
DHT dht(DHTPin, DHTTYPE); // Construct DHT Object for gathering data              
float Temperature; 
float Humidity;

// WIFI settings (MODIFY TO YOUR WIFI SETTINGS!)
const char* ssid = "your_ssid";
const char* password = "your_password";

// MQTT settings (MODIFY TO APPROPRIATE BROKER AND LOGIN CREDENTIALS!)
const char* mqtt_server = "your_broker";
const char* mqtt_username = "your_user" ; 
const char* mqtt_passwd = "your_password" ; 
const char* outTopic = "dbt1/username/dht11/values";  // set a unique topic by setting a username here! 
const char* statusTopic = "dbt1/username/dht11/status"; // set a uniqie topic by setting a username here! 
const String clientId = "jreichwald-esp8266-1";

// JSON-Document 
const size_t capacity = JSON_OBJECT_SIZE(6); // Increase size if you want to transmit larger documents 
DynamicJsonDocument doc(capacity);

WiFiClient espClient;  // The WIFI Client 
PubSubClient client(espClient); // The MQTT client 

#define MSG_BUFFER_SIZE  (256) // Define the message buffer max size 
char msg[MSG_BUFFER_SIZE]; // Define the message buffer 

/**
 * This function will be called when attempting connections to the 
 * WiFi. DO NOT TOUCH UNTIL YOU KNOW WHAT YOU'RE DOING! 
 */
void setup_wifi() {
  delay(50);  
  // Write some debug output to the console ...
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  // Start connection attempts 
  WiFi.begin(ssid, password);

  // As long as we're not connected, try again ....
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  
  randomSeed(micros());

  // show some debug information on serial console 
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());  // IP-Adress is obtained by DHCP, so write it to the console.
}


/**
 * This function is called when we need to reconnect to the MQTT server.
 * ALSO DO NOT TOUCH UNTIL YOU KNOW WHAT YOU'RE DOING! 
 */
void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
     
    // Attempt to connect
    if (client.connect(clientId.c_str(), mqtt_username, mqtt_passwd, statusTopic, 0, true, "OFFLINE")) {
      Serial.println("connected");
      client.publish(statusTopic, "ONLINE", true); 
      
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

/**
 * Callback-Function for incoming messags 
 */
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.println("callack called."); 
}

/**
 * This function is called prior to sending data to mqtt. 
 * The JSON document gets cleared first (to free memory and 
 * avoid memory leaks), then sensor name, timestamp and 
 * measured values (humidity and temperature) are set to 
 * the JSON document.
 */
void setJSONData(float humidity, float temp) { 
  doc.clear();
  doc["sensor"] = "DHT11"; 
  doc["time"] = timeClient.getFormattedTime(); 
  doc["humidity"] = humidity; 
  doc["temperature"] = temp; 
}

/**
 * The setup function is called when the esp is powered on
 */
void setup() {
  Serial.begin(115200);  // Set serial connection to 115200bps 
  pinMode(DHTPin, INPUT); // Set DHT-Pin to INPUT-Mode (so we can read data from it) 
  dht.begin();            
  setup_wifi();          // Call setup_wifi function 
  timeClient.begin(); 
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

/*
 * This is the main program loop. 
 * Evetything is called from here.
 */
void loop() {
  // While the mqtt-connection is not established, 
  // try to reconnect. 
  if (!client.connected()) {
    reconnect();
  }

  // receive measured values from DHT11 
  Temperature = dht.readTemperature(); // Gets the values of the temperature
  Humidity = dht.readHumidity(); // Gets the values of the humidity 

  // set measured data to preprared JSON document 
  setJSONData(Humidity, Temperature); 

  // serialize JSON document to a string representation 
  serializeJsonPretty(doc, msg);   

  // publish to MQTT broker 
  client.publish(outTopic, msg);
  client.loop();
  timeClient.update();

  delay(1000);
}
