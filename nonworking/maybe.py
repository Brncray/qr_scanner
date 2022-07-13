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
exitLoop = False
scanComplete = False
scanCounter = 0

        
def newScan():
    ##start video scan
    global scanCounter
    scanCounter += 1
    print("Start video scan")
    ret, frame = video.read()
    print("Video scan started")
    ##call decoder
    print("Call decoder")    
    decoder(frame, BarCodeData)
    cv2.imshow('Image', frame)
    code = cv2.waitKey(1)
    if code == ord('q'):
        print("error")
        ##break
    
    
    
def after_request(BarCodeData):
    global scanComplete
    global exitLoop
    print(scanComplete)
    print(BarCodeData + " found.")
    os.environ['TZ'] = 'EST+05EDT,M4.1.0,M10.5.0'
    time.tzset()
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    log = {BarCodeData:current_time}
    print("Current Time =", current_time)
    while scanComplete == False:
        inputReturn = input("Press 'r' when returning")
        if inputReturn == "r":
            returning_time = datetime.now()
            returning_current_time = returning_time.strftime("%Y-%m-%d %H:%M:%S")
            return_log = {BarCodeData:current_time, "returned: ": returning_current_time}
            print("Return Time =", returning_current_time)
            info = [BarCodeData, ":", current_time, "returned: ", returning_current_time]
            scanComplete = True
            print("Scan done")
            print(scanComplete)
            exitLoop = True
            with open('logs.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(info)
            new_scan()
            scanCounter = scanCounter + 1
            break
        else:
            print("?????????????????????????????????????????????????")
            break

def decoder(image, BarCodeData):
        
    if exitLoop == False:
        print("Decoder called")
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
                    print("Name not found, please contact admin for help!!!!!!!!!!!!!!!!!!!!!!!!")


              
if __name__ == "__main__":
    ##1st run
    if scanCounter <= 2:
        video = cv2.VideoCapture(0)
        exitLoop = False
        print("Start new scan")
        newScan()
    ##2nd run
    if scanCounter == 2:
        cv2.destroyAllWindows()
    

