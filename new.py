import cv2
import numpy as np
import pyzbar
from pyzbar.pyzbar import decode      
import time 
import logging
import json
import os
from datetime import datetime
import csv
import sys
BarCodeData = ""

names = ["bobrien27", "seriksson", "mmorales", "aciotti", "oseldon", "tmchugh", "dgarrido", "cdeoliveira"]
scanComplete = False

while (scanComplete == False):

    def after_request(BarCodeData):
        print(BarCodeData + " found.")
 
        os.environ['TZ'] = 'EST+05EDT,M4.1.0,M10.5.0'
        time.tzset()
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        log = {BarCodeData:current_time}
        print("Current Time =", current_time)

 
 
        inputReturn = input("Press 'r' when returning")
    
        if inputReturn == "r":
            scanComplete = True
            returning_time = datetime.now()
            returning_current_time = returning_time.strftime("%Y-%m-%d %H:%M:%S")
            return_log = {BarCodeData:current_time, "returned: ": returning_current_time}
            print("Current Time =", returning_current_time)
            info = [BarCodeData, ":", current_time, "returned: ", returning_current_time]
            with open('logs.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(info)
                sys.stdout.flush()
                os.execv(sys.argv[0], sys.argv)
        
        


    def decoder(image, BarCodeData):
    # We're using BGR color format
        trans_img = cv2.cvtColor(image,0)
        BarCode = decode(trans_img)

        for obj in BarCode:
            points = obj.polygon
            (x,y,w,h) = obj.rect
            pts = np.array(points, np.int32)
            # box size
            pts = pts.reshape((-1, 1, 2))
            thickness = 2
            isClosed = True
            # fill color (border)
            line_color = (0, 0, 255)
            cv2.polylines(image, [pts], isClosed, line_color, thickness)
        
        
            # read qr codes (detect and decode qr codes)
            BarCodeData = obj.data.decode("utf-8")
            BarCodeType = obj.type
            the_text = "Data: " + str(BarCodeData)
        
            org = (x,y)
            text_color = (0, 255, 0)
            font = cv2.FONT_HERSHEY_COMPLEX_SMALL
            cv2.putText(image, the_text, org, font, 0.9, text_color, 2)
            # data print 
            print("The Data is: " + BarCodeData +" & the Type is: " + BarCodeType)
        
            for x in range (0,8):
                if(names[x].upper() == BarCodeData.upper()):
                  after_request(BarCodeData)
                  break
            else: 
              print("Name not found, please re-enter")
          
          
    if __name__ == "__main__":
        video = cv2.VideoCapture(0)
        while True:
            ##start video scan
            ret, frame = video.read()
            ##call decoder
            decoder(frame, BarCodeData)
            cv2.imshow('Image', frame)
            code = cv2.waitKey(1)
            if code == ord('q'):
                break


 
        cv2.destroyAllWindows()
    
    
