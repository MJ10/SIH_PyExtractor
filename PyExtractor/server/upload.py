from server import models
import server.demo
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import _thread
import os.path
from datetime import datetime

from utilities.zip_extract import zip_extract
from utilities.location import getData
from server.models import DEPARTMENTS, Account, asset
from server.forms import UploadForm
from server.views import parse_session
from server import views

DATE_FORMAT = '%Y:%m:%d %H:%M:%S'


# GET request to load template
def upload(request):
    authentication_result = views.authentication_check(request)
    if authentication_result is not None:
        return authentication_result
    template_data = parse_session(
        request,
        {'form_button':'Upload'}
    )
    #print(request.user)
    if request.method == 'POST' and request.FILES['zip']:
        # TODO : Wrap everything in a new process
            print(request.user)
            account = Account.objects.get(user=request.user)
            #print(account.role)

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
            _thread.start_new_thread(extract_data, (zip_f, path, request.user, account.role))
            # # Stores list of metadata for uploaded images 
            # # TODO : extend to include other metadata
            # metadata = []

            # # TODO : Extract Metadata from images
            # for file in os.listdir(dest_path):            
            #     # TODO : Change for other file types
            #   if(file.find('.jpg')):  
            #       gps = getGPS(os.path.join(dest_path,file))
            #       metadata.append(gps)
            
            # print(metadata)
            form = UploadForm()
            template_data['form'] = form
            template_data['alert_success'] = "Successfully uploaded. Please wait while we extract data from the image and make it available"
            return render(request, 'upload.html', template_data)
    else:
        form = UploadForm()
    template_data['form'] = form
    return render(request, 'upload.html', template_data) #without context info

#POST request to send zip to server
# def upload(request):
    	
#     # Check if a file is sent
#     if request.method == 'POST' and request.FILES['zip']:
        
#         # TODO : Wrap everything in a new process

#         zip = request.FILES['zip']
#         fs = FileSystemStorage()

#         # To make a subfolder of same name
#         foldername = zip.name.split(".")[0]

#         # a.zip will be stored in media/a/a.zip
#         file = fs.save(os.path.join(foldername,zip.name), zip)
#         path = os.path.join("media",file)
#         print(file + " stored in " + path)

#         # TODO : Extract images from uploaded zip
#         dest_path = os.path.join("media",foldername)
#         print("Extracted images in " + dest_path)
#         zip_extract(path, dest_path)

#         # Stores list of metadata for uploaded images 
#         # TODO : extend to include other metadata
#         metadata = []

#         # TODO : Extract Metadata from images
#         for file in os.listdir(dest_path):            
#             # TODO : Change for other file types
#         	if(file.find('.jpg')):  
#         		gps = getGPS(os.path.join(dest_path,file))
#         		metadata.append(gps)
        
#         print(metadata)

#         return render(request, 'upload.html', {
#             'uploaded_file_url': path
#         })

    return render(request, 'upload.html')

def extract_data(zip_f, path, owner, role):
    foldername = zip_f.name.split(".")[0]
    dest_path = os.path.join("media", foldername)
    print("Extracted images in " + dest_path)
    zip_extract(path, dest_path)
    try:
        if os.path.isfile(path):
            print('HERE')
            os.unlink(path)
    except Exception as e:
        print(e)

    if os.path.isfile(path):
        print('There')

    # Stores list of metadata for uploaded images 
    # TODO : extend to include other metadata
    #print(request)
    #metadata = []
    index = 0
    extracted_text = server.demo.segment_images(os.path.join("media",foldername))
    #print(len(extracted_text))
    # TODO : Extract Metadata from images
    print(os.listdir(dest_path))
    for file in os.listdir(dest_path): 
        # TODO : Change for other file types
        if(file.find('.jpg')):
            gps = getData(os.path.join(dest_path,file))
            if not gps['dateTaken']:
                continue
            date = datetime.strptime(str(gps['dateTaken']), DATE_FORMAT)
            print(date.strftime('%Y-%m-%d %H:%M:%S'))
            #print(gps)
            metadata = []
            # print(type(gps))
            if gps['latitude'] is not None:
                metadata =asset(
                    latitude= gps['latitude'],
                    longitude= gps['longitude'],
                    img_name= file, 
                    img_path= os.path.join(dest_path,file),
                    time= date.strftime('%Y-%m-%d %H:%M:%S'),
                    owner= owner,
                    department = role,
                    extracted_text = extracted_text[index]
                )
                #print(metadata)
                index = index + 1
                metadata.save()
            else:
                metadata =asset(
                    latitude= None,
                    longitude= None,
                    img_name= file, 
                    img_path= os.path.join(dest_path,file),
                    time = str(date.strftime('%Y-%m-%d %H:%M:%S.000000')),
                    owner= owner,
                    department = role,
                    extracted_text = extracted_text[index]
                )
                index = index + 1
                metadata.save()
        if index == len(extracted_text):
            break
    #print(extracted_text)
    #print(metadata)

    # return render(request, 'upload.html', {
    #     'uploaded_file_url': path
    # })
