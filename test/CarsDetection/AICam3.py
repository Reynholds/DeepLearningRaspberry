import numpy as np
import cv2 as cv
import time

# Load the Model 
net = cv.dnn.readNet('pedestrian-and-vehicle-detector-adas-0001.xml', 'pedestrian-and-vehicle-detector-adas-0001.bin')

# Specify target device
net.setPreferableTarget(cv.dnn.DNN_TARGET_MYRIAD)

# Read an image
cap = cv.VideoCapture(0)

#image dimension
heigh = 640
width = 1280

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
           cv.rectangle(frame, (xmin, ymin), (xmax, ymax), color=(0, 0, 255), thickness=5)
        elif confidence > 0.3 :
           cv.rectangle(frame, (xmin, ymin), (xmax, ymax), color=(255,0,0), thickness=5)
        elif confidence > 0.05 :
           cv.rectangle(frame,(xmin, ymin) , (xmax, ymax), color=(0,255,0), thickness=5)


    # resize the image
    frame = cv.resize(frame,(width,heigh))


    #end time
    end = time.time()

    # Time elapsed
    seconds = end - start
    fps = seconds / 60

    cv.putText(frame, "FPS : {0:.2f} ".format(str), (10,10), cv.FONT_HERSHEY_COMPLEX, 3, (0,0,0), thickness = 5)
    

    # Display the resulting frame
    cv.imshow('AI Cam', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
