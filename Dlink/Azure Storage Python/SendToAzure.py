import os
import re
import uuid, sys
from azure.storage.blob import BlockBlobService, PublicAccess

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
        local_file_name = right(full_path_to_file, len(full_path_to_file) - full_path_to_file.rfind("Capture"))# input("Enter file name to upload : ")
        #full_path_to_file =os.path.join(local_path, local_file_name)

        # Write text to the file.
        #file = open(full_path_to_file,  'w')
        #file.write("Hello, World!")
        #file.close()
		
        year = mid(filename, 7, 4)
        month = mid(filename, 11, 2)
        day = mid(filename, 13, 2)
        hour = mid(filename, 16, 2)

        print("Temp file = " + full_path_to_file)
        print("\nUploading to Blob storage as blob " + local_file_name)
		
		

        # Upload the created file, use local_file_name for the blob name
        block_blob_service.create_blob_from_path(container_name,  year+"\\"+month+"\\"+day+"\\"+hour+"\\"+local_file_name, full_path_to_file)
        
        os.move(full_path_to_file, full_path_to_file. )
       
    except Exception as e:
        print(e)

path = os.getcwd()

files = []

# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.mp4' in file:
            files.append(os.path.join(r, file))

for f in files:
    print(f)
    filename = right(f, len(f) - f.rfind("Capture"))
    print(filename)
    run_sample(f)