from django.shortcuts import render
from server import models

def upload(request):

	return render(request, 'upload.html')

