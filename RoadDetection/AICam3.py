import numpy as np
import cv2 as cv
import time

# dotted rectangle https://stackoverflow.com/questions/26690932/opencv-rectangle-with-dotted-or-dashed-lines 


# Load the Model 
net = cv.dnn.readNet('person-vehicle-bike-detection-crossroad-0078-FP32.xml', 'person-vehicle-bike-detection-crossroad-0078-FP32.bin')

# Specify target device
net.setPreferableTarget(cv.dnn.DNN_TARGET_MYRIAD)

# Read an image
cap = cv.VideoCapture(0)

#image dimension
heigh = 640
width = 1280

blue = (255,0,0)
green = (0,255,0)
red = (0,0,255)

ColorDetection =[blue, green, red]

while(True):
    # Start time
    start = time.time() 
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Prepare input blob and perform an inference
    blob = cv.dnn.blobFromImage(frame, size=(672, 384), ddepth=cv.CV_8U)
    net.setInput(blob)
    out= net.forward()

    # Draw detected faces on the frame
    for detection in out.reshape(-1, 7):
        confidence = float(detection[2])
        xmin = int(detection[3] * frame.shape[1])
        ymin = int(detection[4] * frame.shape[0])
        xmax = int(detection[5] * frame.shape[1])
        ymax = int(detection[6] * frame.shape[0])
		
        if confidence > 0.5 :
           cv.rectangle(frame, (xmin, ymin), (xmax, ymax), ColorDetection[detection[1]], thickness=5)
        elif confidence > 0.3 :
           cv.rectangle(frame, (xmin, ymin), (xmax, ymax), ColorDetection[detection[1]], thickness=2)
        elif confidence > 0.05 :
           cv.rectangle(frame,(xmin, ymin) , (xmax, ymax), ColorDetection[detection[1]], thickness=1)


    # resize the image
    frame = cv.resize(frame,(width,heigh))


    #end time
    end = time.time()

    # Time elapsed
    seconds = end - start
    fps = 1 / seconds 

    cv.putText(frame, "FPS : {0:.2f} ".format(str), (30,30), cv.FONT_HERSHEY_COMPLEX, 3, (0,0,0), thickness = 5)
    

    # Display the resulting frame
    cv.imshow('AI Cam', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()


