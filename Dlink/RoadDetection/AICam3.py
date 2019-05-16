import numpy as np
import cv2 as cv
import time
import datetime

def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, offset, amount):
    return s[offset:offset+amount]


# dotted rectangle https://stackoverflow.com/questions/26690932/opencv-rectangle-with-dotted-or-dashed-lines 

video_prefix = "FTPClip"
file_full_name = '/home/pi/Camera/sended/FTPClip20190511_144507.mp4'
filename =  right(file_full_name, len(file_full_name) - file_full_name.rfind(video_prefix))
year  = int(mid(filename, len(video_prefix), 4))
month = int(mid(filename, len(video_prefix) +4, 2))
day   = int(mid(filename, len(video_prefix) +4 +2, 2))
hour  = int(mid(filename, len(video_prefix) +4 +2 +2 +1, 2))
minute= int(mid(filename, len(video_prefix) +4 +2 +2 +1 +2, 2))
second= int(mid(filename, len(video_prefix) +4 +2 +2 +1 +2 +2, 2))

#print("{}-{}-{} {}:{}:{}".format(int(year),int(month), int(day), int(hour), int(minute), int(second)))
#print("{}-{}-{} {}:{}:{}".format(year,month, day, hour, minute, second))


# Load the Model 
net = cv.dnn.readNet('person-vehicle-bike-detection-crossroad-0078-FP32.xml', 'person-vehicle-bike-detection-crossroad-0078-FP32.bin')

# Specify target device
net.setPreferableTarget(cv.dnn.DNN_TARGET_MYRIAD)

# Read an image
cap = cv.VideoCapture(file_full_name)

#image dimension
width = 1280
heigh = 640

#Setting the frame jump
time_length = cap.get(7)/cap.get(5)
number_frames= cap.get(7)
fps = cap.get(5)
frame_jump = 20
frame_seq = - frame_jump

blue = (255,0,0)
green = (0,255,0)
red = (0,0,255)
white = (255,255,255)
black = (0,0,0)

label = ("Pieton", "Vélo", "Voiture")

ColorDetection =[blue, green, red, white, black]


start_datetime = datetime.datetime.now()

#Create output file
txt_file = open(file_full_name.replace(".mp4",".txt"), 'w+')
txt_file.write('{{\n  "record": {{\n    "time_length" : {0},\n    "fps": {1},\n    "frame_jump" : {2},\n    "width" : {3},\n    "heigh" : {4},\n    "start_time" : "{5}",\n    "detections" :[\n'.format(time_length, fps, frame_jump, width, heigh, start_datetime))


while(True):
    # Start time
    start = time.time() 
    
    # Get a specific number of frame
    frame_seq += frame_jump 
    frame_no = (frame_seq /number_frames)
    if frame_seq > number_frames :
        break
    cap.set(1,frame_seq)
    
    
    # Capture specific frame
    ret, frame = cap.read()
    
    print ("{4} : frame n°{0}/{1} -> frame_no = {2} at {3}".format(frame_seq,number_frames,frame_no,cap.get(0)/1000, datetime.datetime.now()) )     
    # Prepare input blob and perform an inference
    blob = cv.dnn.blobFromImage(frame, size=(1024,1024), ddepth=cv.CV_8U)
    net.setInput(blob)
    ## RREI Note : 1er lancement de cette instruction longue
    out= net.forward()
    
    
    # Draw detected faces on the frame
    for detection in out.reshape(-1, 7):
        confidence = float(detection[2])
        xmin = int(detection[3] * frame.shape[1])
        ymin = int(detection[4] * frame.shape[0])
        xmax = int(detection[5] * frame.shape[1])
        ymax = int(detection[6] * frame.shape[0])
     
     
        if confidence > 0.5 :        
          #Ecriture au format : ['frame':3, 'detection':'voiture', 'confiance':50, 'horodatage':'2019-05-14 13:45:59', position:[xmin=0,ymin=0,xmax=5,ymax=5]]
           print("{{'frame':{0}, 'detection':'{1}' 'confiance':{2}, 'horodatage':'{3}', position:['xmin':{4},'ymin':{5},'xmax':{6},'ymax':{7}]}}\n".format(frame_no*number_frames, label[int(detection[1])], detection[2]*100, datetime.datetime.fromtimestamp(cap.get(0)/1000  + datetime.datetime(year, month, day, hour, minute, second, 0).timestamp()) , detection[3]* frame.shape[1],detection[4]* frame.shape[0],detection[5]* frame.shape[1],detection[6]* frame.shape[0]))
           txt_file.write('        {{"frame":{0}, "detection":"{1}", "confiance":{2}, "horodatage":"{3}", "position":{{"xmin":{4},"ymin":{5},"xmax":{6},"ymax":{7}}}}},\n'.format(frame_no*number_frames, label[int(detection[1])], detection[2]*100, datetime.datetime.fromtimestamp(cap.get(0)/1000  + datetime.datetime(year, month, day, hour, minute, second, 0).timestamp()) , detection[3]* frame.shape[1],detection[4]* frame.shape[0],detection[5]* frame.shape[1],detection[6]* frame.shape[0]))
           #cv.rectangle(frame, (xmin, ymin), (xmax, ymax), ColorDetection[int(detection[1])], thickness=5)
        elif confidence > 0.35 :
           #cv.rectangle(frame, (xmin, ymin), (xmax, ymax), ColorDetection[int(detection[1])], thickness=2)
        elif confidence > 0.15 :
           #cv.rectangle(frame,(xmin, ymin) , (xmax, ymax), ColorDetection[int(detection[1])], thickness=1)


    # resize the image
    #frame = cv.resize(frame,(width,heigh))


    #end time
    end = time.time()

    # Time elapsed
    seconds = end - start
    fps = 1 / seconds 

    #cv.putText(frame, "FPS : {0:.2f} ".format(fps), (30,30), cv.FONT_HERSHEY_COMPLEX, 1, (0,0,0), thickness = 1)
    

    # Display the resulting frame
    #cv.imshow('AI Cam', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
end_datetime = datetime.datetime.now()
duration = divmod((end_datetime- start_datetime).total_seconds(), 60)
txt_file.write('        {{"EndOfDetections":true}}],\n    "end_time":"{}",\n    "duration":"{}"\n }} \n}}'.format(datetime.datetime.now(), duration))   
txt_file.close()
cv.destroyAllWindows()


