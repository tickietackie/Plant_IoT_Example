#if defined(ESP8266)
#include <ESP8266WiFi.h>  // included in standard library 
#elif defined(ESP32)
#include "WiFi.h"
#else
#error Unsupported hardware
#endif

#include <PubSubClient.h> // Install PubSubClient via Library Manager 
#include <DHT.h> // Install DHT Sensor Library via Library Manager 
#include <ArduinoJson.h> // Install ArduinoJson via Library Manager 
#include <NTPClient.h> // Install NTPClient Library via Library Manager 
#include <WifiUdp.h> // included in standard library 
#include "secret.h"   //maybe has to be changed to the local path

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

#if defined(ESP8266)
uint8_t DHTPin = D1;  // DHT11-Sensor connected to Pin D1 (VCC should be connected to 3,3V, GRN to GRN)
DHT dht(DHTPin, DHTTYPE); // Construct DHT Object for gathering data
#elif defined(ESP32)
// DHT Sensor (Reference-Architecture from lecture)
#define DHTPin 13
DHT dht(DHTPin, DHT11); // Construct DHT Object for gathering data
#else
#error Unsupported hardware
#endif

float Temperature;
float Humidity;

// WIFI settings (MODIFY TO YOUR WIFI SETTINGS!)
const char ssid[] = SECRET_SSID;       // your network SSID (name)
const char password[] = SECRET_PASS;       // your network password (use for WPA, or use as key for WEP)

// MQTT settings (MODIFY TO APPROPRIATE BROKER AND LOGIN CREDENTIALS!)
const char mqtt_server[] = MQTT_SERVER;
const char mqtt_username[] = MQTT_USERNAME;
const char mqtt_passwd[] = MQTT_PASSWD;
const char outTopic[] = OUT_TOPIC;
const int mqtt_port = 1883;
const char* statusTopic = "dbt1/plantDataGroup5/dht11/status"; // set a uniqie topic by setting a username here!
const String clientId = CLIENT_ID;
String areaId = "";

// JSON-Document
const size_t capacity = JSON_OBJECT_SIZE(2500); // Increase size if you want to transmit larger documents
DynamicJsonDocument doc(capacity);

WiFiClient espClient;  // The WIFI Client
PubSubClient client(espClient); // The MQTT client

#define MSG_BUFFER_SIZE (4000) // Define the message buffer max size 
char msg[MSG_BUFFER_SIZE]; // Define the message buffer

unsigned long locationId = 0;

/**
   This function will be called when attempting connections to the
   WiFi. DO NOT TOUCH UNTIL YOU KNOW WHAT YOU'RE DOING!
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

  areaId = WiFi.macAddress();

  if (areaId == "08:3A:F2:AA:85:44") {  //Steffen
    locationId = 0;
  }
  else if (areaId == "8C:AA:B5:7C:F9:86") {   //Kai
    locationId = 1;
  }
  else if (areaId == "08:3A:F2:6E:29:A8") {   //Marvin
    locationId = 2;
  }
  else if (areaId == "AC:67:B2:37:82:C0") { //Mehmet
    locationId = 3;
  }
  else {
    Serial.println("location could not be found for mac address: ");
    Serial.println("Fatal error. abort.");
    const int i = 0;
    while (i == 0) {
      const int stayHere = 0;
    }
  }

  // if analog input pin 0 is unconnected, random analog
  // noise will cause the call to randomSeed() to generate
  // different seed numbers each time the sketch runs.
  // randomSeed() will then shuffle the random function.
  randomSeed(analogRead(0));

  // show some debug information on serial console
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());  // IP-Adress is obtained by DHCP, so write it to the console.*/
}



/**
   This function is called when we need to reconnect to the MQTT server.
   ALSO DO NOT TOUCH UNTIL YOU KNOW WHAT YOU'RE DOING!
*/
void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");

    // Attempt to connect
    if (client.connect(clientId.c_str(), mqtt_username, mqtt_passwd, statusTopic, 0, true, "OFFLINE")) {
      Serial.println("connected");
      //client.publish(statusTopic, "ONLINE", true);
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
   Callback-Function for incoming messags
*/
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.println("callback called.");
  Serial.print("Payload: ");
  Serial.println((char*)payload);
}

/**
   This function is called prior to sending data to mqtt.
   The JSON document gets cleared first (to free memory and
   avoid memory leaks), then sensor name, timestamp and
   measured values (humidity and temperature) are set to
   the JSON document.
*/
void setJSONData(float humidity, float temp, float soil) {
  doc.clear();
  doc["transport_id"] = random(2147483647); //Max random value between 0 and 2147483647, 32 bit
  doc["location_id"] = locationId;
  doc["area_id"] = areaId;
  doc["time"] = timeClient.getEpochTime();

  StaticJsonDocument<600> docArray;
  
  // create an empty array
  JsonArray array = docArray.to<JsonArray>();

  StaticJsonDocument<200> sensorDoc;
  JsonObject sensor = sensorDoc.createNestedObject("DHT11");
  sensor["value"] = temp;
  sensor["unit"] = "C";
  sensor["type"] = "temperature";
  sensor["name"] = "DHT11";
  
  // add some values
  array.add(sensor);

  sensor["value"] = humidity;
  sensor["unit"] = "%";
  sensor["type"] = "humidity";
  sensor["name"] = "DHT11";

  array.add(sensor);

  sensor["value"] = 0;
  sensor["unit"] = "1";
  sensor["type"] = "soil";
  sensor["name"] = "hygrometer";

  array.add(sensor);

  doc["sensor"] = array;

}

/*
   json should have sensors in array and then for each sensor the value
*/


/**
   The setup function is called when the esp is powered on
*/
void setup() {
  Serial.begin(115200);  // Set serial connection to 115200bps

  pinMode(DHTPin, INPUT); // Set DHT-Pin to INPUT-Mode (so we can read data from it)
  dht.begin();
  setup_wifi();          // Call setup_wifi function
  timeClient.begin();
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

/*
   This is the main program loop.
   Everything is called from here.
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
  //Temperature = 10;
  //Humidity = 5;
  // set measured data to preprared JSON document
  const float soil = 0;
  setJSONData(Humidity, Temperature, soil);

  // serialize JSON document to a string representation
  serializeJson(doc, msg);
  serializeJsonPretty(doc, Serial);

  // publish to MQTT broker
  client.publish(outTopic, msg);
  client.setBufferSize(512);
  client.loop();
  timeClient.update();

  delay(5000);
}
