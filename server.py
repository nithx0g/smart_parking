import paho.mqtt.client as mqtt
import threading
import asyncio
import websockets
import time
import datetime
class Server:
    def __init__(self,slots):
        self.slots = slots #parking slots
        self.client = mqtt.Client("Server",protocol=mqtt.MQTTv5)
        self.client.tls_set("ca.crt")
        self.client.tls_insecure_set(True)

        thread = threading.Thread(target=self.server,args=()) # to keep running continously
        thread.daemon = True
        thread.start()
    
    def server(self):
        def on_connect(client,userdata,a,b,c): #when connected
            topics = [("PARK",0),("EXIT",0)]
            time.sleep(0.25)
            self.client.subscribe(topics) #subscribe to PARK and EXIT
            time.sleep(0.25)

        async def send_to_camera(message):
            uri = "ws://localhost:9999"  # uri of camera
            async with websockets.connect(uri) as websocket:
                await websocket.send(message)
                car_number = await websocket.recv()  # receive car number
                return car_number
        def on_message(client,userdata,message):  #on receiving message
            if(message.topic == "PARK"): #if message received from PARK topic
                time.sleep(0.5)
                car_number = asyncio.run(send_to_camera(message.payload.decode("utf-8")))  #send to camera for ocr
                self.slots[int(message.payload.decode("utf-8"))] = str(car_number) #add car number to slot
                f = open("logs/parking_log.txt","a")  #adding to logs
                f.write(str(datetime.datetime.now()) + " car " + str(car_number) + " parked at " + str(message.payload.decode("utf-8")) + "\n")
                f.close()

            if(message.topic == "EXIT"): #if message received from EXIT topic
                time.sleep(0.5)
                f = open("logs/parking_log.txt","a") # adding to logs
                f.write(str(datetime.datetime.now()) + " car " + str(self.slots[int(message.payload.decode("utf-8"))]) + " exited at " + str(message.payload.decode("utf-8")) + "\n")
                f.close()
                self.slots[int(message.payload.decode("utf-8"))] = ""  #empty slot
        
        
        self.client.on_message = on_message
        self.client.on_connect = on_connect

        self.client.username_pw_set(username="server",password="password") #authenticate
        self.client.connect("127.0.0.1") #port 1883
        
        self.client.loop_forever()
        

            
    
    


