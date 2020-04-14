# ESP32-connection-with-MQTT-python-interface-tkinter
![Topic Configuration](https://github.com/FreakJazz/ESP32-connection-with-MQTT-python-interface-tkinter/blob/master/images/hiveMQ.JPG)
![Topic Configuration](https://github.com/FreakJazz/ESP32-connection-with-MQTT-python-interface-tkinter/blob/master/images/publicMQTT.JPG)

## Description

This program works with MQTT conection of  IOT in order to turn on light in ESP32 from  a desktop app with Tkinter.

## Contents

- Description
- Contents
- Library Installation
- Broker
- Programation
- Results
- Contributing

## Library Installation

In order to create a MQTT connection with Python 
We have to install *pip install paho-mqtt*
[Paho Library](https://pypi.org/project/paho-mqtt/)

### Installation
The latest stable version is available in the Python Package Index (PyPi) and can be installed using

``` pip install paho-mqtt```
Or with virtualenv:

``` 
virtualenv paho-mqtt
source paho-mqtt/bin/activate
pip install paho-mqtt 
```

## Broker

After that, We need to open a Broker HIVEMQ
[Broker Address](https://www.hivemq.com/public-mqtt-broker/)

The following parameters must be considered to establish the connection
![Topic Configuration](https://github.com/FreakJazz/ESP32-connection-with-MQTT-python-interface-tkinter/blob/master/images/broker.JPG/)
- **Host:**     broker.mqttdashboard.com
- **Port:**     1883 (Web Port)
- **ClientID:** This parameter is given by the user
- **Username:** This parameter is given by the user
- **Password:** This parameter is given by the user
- **Topic:**    This parameter is given by the user

## Programation

### Python

#### Configure

In order to create a desktop application, the Tkinter Framework which is already installed in Python was used, so only the necessary libraries will be called to make the application.

``` python
###### IMPORT LYBRARIES ########
import ssl                          # Establish secure connection
import sys
import paho.mqtt.client as mqtt    # Connect with the MQTT Library
import time                         # Time Library  
from tkinter import *
from tkinter import ttk, font       # Import Tkinter Lybrary
from tkinter import messagebox
import getpass
```
#### Main

``` python
# Main program
if __name__ == "__main__":                  # Especial function main
    window = Tk()                       # Define window interface
    application = App(window)             # 
    window.mainloop() 
```

#### General Class

Principal class
```python
class App(ttk.Frame):

    # Window Init
    def __init__(self, window):
```

#### MQTT

Connection is stablish with:

```python
self.host = "broker.mqttdashboard.com"
self.port 1883;
self.keepalive = 60;
self.clientid = "ClientID";
self.username = "Your Username";
self.password = "Your Password";
self.topic = "Your Topic";
```
***The same parameters entered in the broker must be established***

Connection Function

``` python
####### FUNCTION ON CONNECT ######
    def on_connect(self,client, userdata, flags, rc):
        print('Connected(%s)',self.client._client_id)
        client.subscribe(self.topic, qos=0) 
        client.publish(self.topic,'Connected')
```

Message Function

``` python
    ####### FUNCTION ON MESSAGE ######
    def on_message(self,client, userdata, message):
        print('----------------------')
        print('topic: %s',  message.topic)
        print('payload: %s', message.payload)
        print('qos: %d', message.qos)
        print(message.payload.decode("utf-8"))
```

Publish 

``` python
self.client.publish(self.topic, state)
```
Disconnected function

```python
self.client.disconnect()
```

### Arduino

The *ESP32* card was programmed using arduino to receive the data and turn on a light using the desktop application made in *Python*

#### Configure

The necessary libraries are shown below

```
#include <WiFi.h>
#include <PubSubClient.h>
```
#### Main

```
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
```
#### MQTT

Connection is stablish with:

```
// Select NODE MQTT
const char* host = "broker.mqttdashboard.com";         //'broker.mqttdashboard.com';
const int port = 1883;
const int keepalive = 60;
const char* clientid = "ClientID";
const char* username = "Your Username";
const char* password = "Your Password";
const char* topic = "Your Topic";
```
***The same parameters entered in the broker must be established***

#### WIFI Connection

Connection is stablish with:
```
    const char* ssid = "WIFI";
    const char* pass = "Password";
```

Connection Function

``` python
####### FUNCTION ON CONNECT ######
    def on_connect(self,client, userdata, flags, rc):
        print('Connected(%s)',self.client._client_id)
        client.subscribe(self.topic, qos=0) 
        client.publish(self.topic,'Connected')
```

## Result

### Desktop App

![Topic Configuration](https://github.com/FreakJazz/ESP32-connection-with-MQTT-python-interface-tkinter/blob/master/images/Interface.JPG)

### MQTT Config

![Topic Configuration](https://github.com/FreakJazz/ESP32-connection-with-MQTT-python-interface-tkinter/blob/master/images/MQTT_Connection.JPG)

### Python Interface Configuration MQTT

![Topic Configuration](https://github.com/FreakJazz/ESP32-connection-with-MQTT-python-interface-tkinter/blob/master/images/python_connection.JPG)

### Topic

MQTT 

![Topic Configuration](https://github.com/FreakJazz/ESP32-connection-with-MQTT-python-interface-tkinter/blob/master/images/topic_message.JPG)

Arduino

![Topic Configuration](https://github.com/FreakJazz/ESP32-connection-with-MQTT-python-interface-tkinter/blob/master/images/arduino_topic.JPG)

### Interface Works

Turn light ON

![Topic Configuration](https://github.com/FreakJazz/ESP32-connection-with-MQTT-python-interface-tkinter/blob/master/images/Interface.JPG)

The light is in GPIO 2 OF ESP32

![Topic Configuration](https://github.com/FreakJazz/ESP32-connection-with-MQTT-python-interface-tkinter/blob/master/images/ESP32_light_ON.jpeg)

Turn light OFF

![Topic Configuration](https://github.com/FreakJazz/ESP32-connection-with-MQTT-python-interface-tkinter/blob/master/images/Interfaceoff.JPG)

The light is in GPIO 2 OF ESP32

![Topic Configuration](https://github.com/FreakJazz/ESP32-connection-with-MQTT-python-interface-tkinter/blob/master/images/ESP32_light_OFF.jpeg)

## Contributing

**JAZMIN RODRIGUEZ** 
[GitHub](https://github.com/FreakJazz)   
[LinkedIn](https://www.linkedin.com/in/jazm%C3%ADn-rodr%C3%ADguez-80b580133/)
