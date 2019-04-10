import requests
import re
import os

cam_protocol = "http://"
cam_address = "192.168.235.99" #"192.168.1.249"#"192.168.235.99"
cam_user = "admin"
cam_password = "InnoveSmartWorld"

regexSearch = 'g_folderslistStr = GV\("(.+?)\);'
regexSearchFile = 'var g_filelistStr = decodeURIComponent\(GV\("(.+?)\)\)'

url_getFolderVideo = "/cgi-bin/sdoperate.cgi?list=&path=/video&page=1"
url_getFolderVideoDate = "/cgi-bin/sdoperate.cgi?list=&path=/video/" #"/cgi-bin/sdoperate.cgi?list=&path=/video/20190212&page=2" 
url_getDownload = "/cgi-bin/sddownload.cgi?file=/video/"  #http://192.168.1.249/cgi-bin/sddownload.cgi?file=/video/20190213/10/Capture20190213_104654.mp4
url_getDelFile = "/cgi-bin/sdoperate.cgi?sdfpp=3&del=/video/" #http://192.168.1.249/cgi-bin/sdoperate.cgi?sdfpp=3&del=/video/20190213/10/Capture20190213_104654.jpg
url_getContent = "/setup_sdlist.htm"

request_base = cam_protocol+cam_user+":"+cam_password+"@"+cam_address


#1 Change content to Get SD_List Folder
r = requests.get(request_base+url_getFolderVideo)
print ("#### Change Content to get FolderVideo ####")
#print(r.text)
r = requests.get(request_base+url_getContent)
print ("#### Show Content to get FolderVideo ####")
#print(r.text)
m = re.search(regexSearch, r.text)
if m:
       found=m.group(1)
       print(found)

       miningFolderDate = found.split(",",-1)
       miningFolderDateFound = miningFolderDate[0].split(";",1)


#2 - For finding folder get the time folder in here
r = requests.get(request_base+url_getFolderVideoDate+miningFolderDateFound[0])
print ("#### Change Content to get FolderVideobyHour ####")
#print(r.text)
r = requests.get(request_base+url_getContent)
print ("#### Show Content to get FolderVideobyHour ####")
#print(r.text)
m = re.search(regexSearch, r.text)
if m:
       found=m.group(1)
       print(found)

       miningFolderHour = found.split(",",-1)
       miningFolderFileVideo = miningFolderHour[0].split(";",1)


#3 - For finding folder hour get the files in here
r = requests.get(request_base+url_getFolderVideoDate+miningFolderDateFound[0]+"/"+miningFolderFileVideo[0])
print ("#### Change Content to get FolderVideoDateHourFile ####")
#print(r.text)
r = requests.get(request_base+url_getContent)
print ("#### Show Content to get FolderVideoDateHourFile ####")
#print(r.text)
m = re.search(regexSearchFile, r.text)
if m:
       found=m.group(1)
       print(found)

       miningFolderFile = found.split(",",-1)
       miningFileVideo = miningFolderFile[1].split(";",1)
       


#4 - Download the video
url_download = request_base+url_getDownload+miningFolderDateFound[0]+"/"+miningFolderFileVideo[0]+"/"+miningFileVideo[0]
r = requests.get(request_base+url_getDownload+miningFolderDateFound[0]+"/"+miningFolderFileVideo[0]+"/"+miningFileVideo[0])

    # Create directory for store the video
dirName = 'download'

if os.path.exists(dirName):
    print("Directory " , dirName ,  " already exists")
else:
    os.mkdir(dirName)

open(dirName+'/'+miningFileVideo[0], 'wb').write(r.content)


#5 - Delete the video and the jpg
r = requests.get(request_base+url_getDelFile+miningFolderDateFound[0]+"/"+miningFolderFileVideo[0]+"/"+miningFileVideo[0])
r = requests.get(request_base+url_getDelFile+miningFolderDateFound[0]+"/"+miningFolderFileVideo[0]+"/"+miningFileVideo[0].replace(".mp4",".jpg"))
