import numpy as np
import cv2 as cv

# Load the Model 
net = cv.dnn.readNet('face-detection-adas-0001.xml', 'face-detection-adas-0001.bin')

# Specify target device
net.setPreferableTarget(cv.dnn.DNN_TARGET_MYRIAD)

# Read an image
cap = cv.VideoCapture(0)


while(True):
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
        if confidence > 0.5:
            cv.rectangle(frame, (xmin, ymin), (xmax, ymax), color=(0, 0, 255), thickness=10)

    # resize the image
    frame = cv.resize(frame,(640,320))

    # Display the resulting frame
    cv.imshow('AI Cam', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()
