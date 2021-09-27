# Plant_IoT_Example

To make it work, create a secret.h file at the .ino file.

secret.h has to look like the following:

```
// Both SSID and password must be 8 characters or longer
#define SECRET_SSID ""  //your ssid
#define SECRET_PASS "" //your wifi password
#define CLIENT_ID "iAmUnique" //change this to a unique client id
#define OUT_TOPIC "plantDataGroup5"
#define MQTT_SERVER ""    //data from Moodle
#define MQTT_USERNAME ""
#define MQTT_PASSWD ""
```

The cred.py hat to look like the following:

```
login = {
    'db_user' : 'user',
    'db_password' : 'pw',
    'host' : 'hostip',
    'database' : 'dbname',
    'port' : 'port',
    'brokeraddress' : 'address',
    'mqtt_user' : 'user',
    'mqtt_password' : 'pw',
    'mqtt_topic' : 'topic',
    'location_name' : 'loc name'
}
```