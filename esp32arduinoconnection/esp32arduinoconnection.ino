#include <WiFi.h>
#include <PubSubClient.h>
 
WiFiClient espClient;
PubSubClient client(espClient);

// Select NODE
const char* host = "broker.mqttdashboard.com";         //'broker.mqttdashboard.com';
const int port = 1883;
const int keepalive = 60;
const char* clientid = "Clientjazz23";
const char* username = "jazz23";
const char* password = "12345";
const char* topic = "light";

// Select NODE
/*const char* host = "ioticos.org";  
const int port = 1883;
const int keepalive = 60;
const char* clientid = "Clientjazz23";
const char* username = "nVzqLcwdpINQj7J";
const char* password = "9bvC3gSQ9gBX8tC";
const char* topic = "jY5fbAqMPqPlUYk";*/

const char* ssid = "NETLIFE-FLIA. RODRIGUEZ";
const char* pass = "172372rodriguez";
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE  (50)
char msg[MSG_BUFFER_SIZE];
int value = 0;

// Led
int led = 2;

void callback(char* topic, byte* payload, unsigned int length) {
  String incoming = "";
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] "); 
  for (int i=0;i<length;i++) {
    incoming += (char)payload[i];
    Serial.print(incoming);
  }
  Serial.println();
  if (incoming=="1"){
    digitalWrite(led,HIGH);
    }
    if (incoming=="0"){
    digitalWrite(led,LOW);
    }
}

// Reconected MQTT fuction
void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    //clientid += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientid, username, password)) {
      Serial.println("Connected");
      // Once connected, publish an announcement...
      client.publish(topic,"Hello");
      // ... and resubscribe
      client.subscribe(topic);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    } 
  }
}

void setup()
{
  // Serial comunication init
  Serial.begin(115200);
  // Wifi Connection
  delay(10);
  Serial.println(" Connecting SSID: ");
  Serial.println(ssid);
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");}
  Serial.println("");
  Serial.println("WIFI Connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());

  // MQTT Connection
  client.setServer(host, port);
  client.setCallback(callback);
  // Allow the hardware to sort itself out
  delay(1500);

  // Output Configuration
  pinMode(led,OUTPUT);
  digitalWrite(led,LOW);

}

void loop()
{
  if (!client.connected()) {
    reconnect();
  }

  if (client.connected()){
     String str = "";
    
    }
  client.loop();
  
}


