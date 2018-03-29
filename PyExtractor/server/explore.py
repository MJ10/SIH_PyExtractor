from django.shortcuts import render
from server import models

def explore(request):

	return render(request, 'explore.html')