import cv2
from cv2 import threshold 
import serial 
import time

arduinoData = serial.Serial("COM4", 9600)

#img = cv2.imread("lena.png")

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

classNames = []
classFiles = "coco.names"

with open(classFiles, "rt") as f:
    classNames = f.read().rstrip("\n").rsplit("\n")

#print(classNames)

weights = "frozen_inference_graph.pb"
models = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"

net = cv2.dnn_DetectionModel(weights, models)
net.setInputSize(320, 320)
net.setInputScale(1.0/127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)



while True:
    
    ret, img = cap.read()
    
    classIds, confs, bbox = net.detect(img, confThreshold=0.5)

    #print(classIds, bbox)

    if len(classIds) != 0:
        for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
            if classId == 1:
                cv2.rectangle(img, box, color=(0,255,0), thickness=2)
                cv2.putText(img, classNames[classId-1].upper(), (box[0]+10, box[1]+30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 1)
                cv2.putText(img, str(round(confidence*100,2)), (box[0]+150, box[1]+30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 1)
                x, y = str(box[0]), str(box[1])
            #print(classId)
                print('Human Detected')
                
                arduinoData.write(b'1')

            else:
                print("No Human Detected")
        
                arduinoData.write(b'0')

            #print("The Coordinated Position is:",(x,y))
            #print(x)
            #arduinoData.write(x.encode())
            #time.sleep(0.5)
            #arduinoData.write(y.encode())
            #print(arduinoData.readline())
            #arduinoSer= arduinoData.readline().decode("ascii")
            #print(arduinoSer)

    

    cv2.imshow("Images", img)

    cv2.waitKey(1)


    