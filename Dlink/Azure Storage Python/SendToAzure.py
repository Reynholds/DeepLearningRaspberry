import os
import glob
import re
import uuid, sys
from azure.storage.blob import BlockBlobService, PublicAccess

video_prefix = "FTPClip"

def left(s, amount):
    return s[:amount]

def right(s, amount):
    return s[-amount:]

def mid(s, offset, amount):
    return s[offset:offset+amount]

def run_sample(full_path_to_file):
    try:
        # Create the BlockBlockService that is used to call the Blob service for the storage account
        block_blob_service = BlockBlobService(account_name='pavic', account_key='lPdOTarDD4n3xuwz5EHMNOK3q/SNpnZ/1FKYKHNJSL4V4ZPt1LlvtjTZlpCfnghYFYQi20nTpBx6GVRPKfghoQ==')

        # Create a container called 'quickstartblobs'.
        container_name ='aicamvideoclips'
        block_blob_service.create_container(container_name)
        #block_blob_service.cre

        # Set the permission so the blobs are public.
        block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)

        # Create a file in Documents to test the upload and download.
        local_path=os.path.abspath(os.path.curdir)
        local_file_name = right(full_path_to_file, len(full_path_to_file) - full_path_to_file.rfind(video_prefix))# input("Enter file name to upload : ")
        #full_path_to_file =os.path.join(local_path, local_file_name)

        # Write text to the file.
        #file = open(full_path_to_file,  'w')
        #file.write("Hello, World!")
        #file.close()
		
        year  = mid(local_file_name, len(video_prefix), 4)
        month = mid(local_file_name, len(video_prefix) +4, 2)
        day   = mid(local_file_name, len(video_prefix) +4 +2, 2)
        hour  = mid(local_file_name, len(video_prefix) +4 +2 +2 +1, 2)

        print("Temp file = " + full_path_to_file)
        print("\nUploading to Blob storage as blob " + local_file_name)
		
		

        # Upload the created file, use local_file_name for the blob name
        block_blob_service.create_blob_from_path(container_name,  year+"\\"+month+"\\"+day+"\\"+hour+"\\"+local_file_name, full_path_to_file)
        
               
        #Move uploaded file to sended directory
        try:
                os.mkdir(path+"//sended")
        except Exception as e:
                print(e)
        os.rename(full_path_to_file, full_path_to_file.replace(video_prefix,"sended/"+video_prefix))
        print("{0} Move to sended\n".format(local_file_name))
         
    except Exception as e:
        print(e)

path = os.getcwd()

files = []

# r=root, d=directories, f = files
#for r, d, f in os.walk(path):
#    for file in f:
#        if '.mp4' in file:
#            files.append(os.path.join(r, file))

files_in_dir = os.listdir(path)
for file in files_in_dir :
    if '.mp4' in file:
            files.append(os.path.join(path, file))

            
print ("\n\t{0} files to send\n".format(len(files)))

for f in files:
    #print(f)
    filename = right(f, len(f) - f.rfind(video_prefix))
    print(filename)
    run_sample(f)
