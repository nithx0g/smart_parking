import paho.mqtt.client as mqtt
import time

class Sensor:
    def __init__(self,id):
        self.id = id  #id of the sensor
        self.client = mqtt.Client("Sensor"+str(id),protocol=mqtt.MQTTv5)
        self.client.tls_set("ca.crt")  #certificate authority
        self.client.tls_insecure_set(True)  #to disable hostname check
    
    #when a car enters
    def entry(self):
        self.client.username_pw_set(username="sensor",password="password") #authentication
        self.client.connect("127.0.0.1") #port 1883
        time.sleep(0.25)
        self.client.publish(topic="PARK",payload=str(self.id)) 
        time.sleep(0.25)
        self.client.disconnect()
    
    #when a car exits
    def exit(self):
        self.client.username_pw_set(username="sensor",password="password")
        self.client.connect("127.0.0.1") #port 1883
        time.sleep(0.25)
        self.client.publish("EXIT",payload=str(self.id))
        time.sleep(0.25)
        self.client.disconnect()

