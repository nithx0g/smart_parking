import websockets
import asyncio
import paho.mqtt.client as mqtt
import random
import threading
import cv2
import numpy as np
import easyocr
import imutils
import time

class Camera:
    def __init__(self):
        self.client = mqtt.Client("Camera")
        thread = threading.Thread(target=self.run,args=()) #new thread keep listening continously
        thread.daemon = True
        thread.start()
    async def ocr(self,i):
        #image segmentation
        img = cv2.imread("images/"+str(i)+".jpg")  #read image
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        bfilter = cv2.bilateralFilter(gray,11,17,17)
        edged = cv2.Canny(bfilter,30,200)   #edge detection filter
        keypoints = cv2.findContours(edged.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #find shapes
        contours = imutils.grab_contours(keypoints)
        contours = sorted(contours,key=cv2.contourArea,reverse=True)[:10]  

        location = None
        for contour in contours:
            approx = cv2.approxPolyDP(contour,10,True)
            if(len(approx) == 4):  #find rectangular contour
                location = approx
                break

        #masking oprinal image
        mask = np.zeros(gray.shape,np.uint8)
        new_image = cv2.drawContours(mask,[location],0,255,-1)
        new_image = cv2.bitwise_and(img,img,cv2.COLOR_BGR2RGB)
        (x,y) = np.where(mask==255)
        (x1,y1) = (np.min(x),np.min(y))
        (x2,y2) = (np.max(x),np.max(y))

        #send cropped image to easyocr
        cropped_image = gray[x1:x2+1,y1:y2+1]
        reader = easyocr.Reader(['en'])
        result = reader.readtext(cropped_image)
        
        return "".join(result[0][-2].split())[-4:] #return car number


    async def scan(self,websocket, path):
        slot_number = await websocket.recv() #receive slot number from server
        i = random.randint(1,3)
        time.sleep(0.25)
        car_number = await self.ocr(i)  # ocr to get car number
        time.sleep(0.25)
        await websocket.send(str(car_number))  #send car number to server

    async def main(self):
        async with websockets.serve(self.scan,"localhost",9999):  # keep listening for connections on this port
            await asyncio.Future()
    
    def run(self):
        asyncio.run(self.main())
    
