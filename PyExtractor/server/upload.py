from server import models
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os.path
from utilities.zip_extract import zip_extract

def upload(request):
	return render(request, 'upload.html')



# GET request to load template
def upload(request):
    return render(request, 'upload.html') #without context info

#POST request to send zip to server
def upload(request):
    	
    # Check if a file is sent
    if request.method == 'POST' and request.FILES['zip']:
        
        zip = request.FILES['zip']
        fs = FileSystemStorage()
        foldername = zip.name.split(".")[0]

        # a.zip will be stored in media/a/a.zip
        file = fs.save(os.path.join(foldername,zip.name), zip)
        path = os.path.join("media",file)
        print(file + " stored in " + path)
        zip_extract(path,foldername)

		# TODO : Extract media/a/a.zip to 
        return render(request, 'upload.html', {
            'uploaded_file_url': path
        })

    return render(request, 'upload.html')