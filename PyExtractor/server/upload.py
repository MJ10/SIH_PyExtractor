from server import models
import server.demo
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import _thread
import os.path

from utilities.zip_extract import zip_extract
from utilities.location import getGPS

# GET request to load template
def upload(request):
    return render(request, 'upload.html') #without context info

#POST request to send zip to server
def upload(request):
    	
    # Check if a file is sent
    if request.method == 'POST' and request.FILES['zip']:
        
        # TODO : Wrap everything in a new process

        zip_f = request.FILES['zip']
        fs = FileSystemStorage()

        # To make a subfolder of same name
        foldername = zip_f.name.split(".")[0]

        # a.zip will be stored in media/a/a.zip
        file = fs.save(os.path.join(foldername,zip_f.name), zip_f)
        path = os.path.join("media",file)
        print(file + " stored in " + path)

        # # TODO : Extract images from uploaded zip
        # dest_path = os.path.join("media",foldername)
        # print("Extracted images in " + dest_path)
        # zip_extract(path, dest_path)

        # # Stores list of metadata for uploaded images 
        # # TODO : extend to include other metadata
        # metadata = []

        # # TODO : Extract Metadata from images
        # for file in os.listdir(dest_path):            
        #     # TODO : Change for other file types
        # 	if(file.find('.jpg')):  
        # 		gps = getGPS(os.path.join(dest_path,file))
        # 		metadata.append(gps)
        
        # print(metadata)
        _thread.start_new_thread(extract_data, (zip_f, path))

        return render(request, 'upload.html', {
            'uploaded_file_url': path
        })

    return render(request, 'upload.html')

def extract_data(zip_f, path):
    foldername = zip_f.name.split(".")[0]
    dest_path = os.path.join("media",foldername)
    print("Extracted images in " + dest_path)
    zip_extract(path, dest_path)

    # Stores list of metadata for uploaded images 
    # TODO : extend to include other metadata
    metadata = []

    # TODO : Extract Metadata from images
    for file in os.listdir(dest_path):            
        # TODO : Change for other file types
        if(file.find('.jpg')):  
            gps = getGPS(os.path.join(dest_path,file))
            metadata.append(gps)
    extracted_text = server.demo.segment_images(os.path.join("media",foldername))
    print(extracted_text)
    print(metadata)

    # return render(request, 'upload.html', {
    #     'uploaded_file_url': path
    # })