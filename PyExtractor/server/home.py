from django.shortcuts import render
from server import models

def home(request):

	return render(request, 'index.html')
