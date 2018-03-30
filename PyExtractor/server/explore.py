from django.shortcuts import render
from server import models
from server.models import asset
from server.forms import QueryForm
import math

radius_of_earth = 6371

def parse_session(request, template_data=None):
    """
    Checks the session for any alert data. If there is alert data, it added to the given template data.
    :param request: The request to check session data for
    :param template_data: The dictionary to update
    :return: The updated dictionary
    """
    if template_data is None:
        template_data = {}
    if request.session.has_key('alert_success'):
        template_data['alert_success'] = request.session.get('alert_success')
        del request.session['alert_success']
    if request.session.has_key('alert_danger'):
        template_data['alert_danger'] = request.session.get('alert_danger')
        del request.session['alert_danger']
    return template_data


def explore(request):
	template_data = parse_session(
		request,
		{'form_button':'Query'}
	)
	if request.method == 'POST':
		form = QueryForm(request.POST)
		if form.is_valid():
			print(form.cleaned_data['department'])
			print(form.cleaned_data['latitude'])
			print(form.cleaned_data['longitude'])
			print(form.cleaned_data['distance'])
			# Query to find images in that range
			find_images(form.cleaned_data['department'],form.cleaned_data['latitude'],form.cleaned_data['longitude'], form.cleaned_data['distance'], form.cleaned_data['choice'], form.cleaned_data['input_text'])
	else:
		form = QueryForm()
	template_data['form'] = form
	return render(request, 'explore.html', template_data)


# Function to find images having the distance which user wants
def find_images(department,latitude,longitude, distance, choice, input_text):
	print(department,latitude,longitude)
	phi1 = toRadians(latitude)
	lambda1 = toRadians(longitude)
	print(phi1,lambda1)

	for asseti in asset.objects.all():
		#print(asseti.img_name,asseti.img_path,asseti.extracted_text,asseti.latitude,asseti.longitude,asseti.department,asseti.time)			
		phi2 = toRadians(asseti.latitude)
		lambda2 = toRadians(asseti.longitude)
		got_distance = getDistance(phi1,phi2,lambda1,lambda2,distance)
		if int(choice) == 0:
			if got_distance < int(distance) and asseti.department == department and asseti.kind == str(input_text):
				print(asseti.img_name)
		else:
			if got_distance < int(distance) and asseti.department == department and asseti.capacity == int(input_text):
				print(asseti.img_name)


# Convert the latitude and longitude to Radians
def toRadians(input):
	return 0.0174533*float(input)

# Get distance between the two points
def getDistance(phi1,phi2,lambda1,lambda2,radius):
	angle = math.acos(math.sin(float(phi1))*math.sin(float(phi2)) + math.cos(float(phi1))*math.cos(float(phi2))*math.cos(abs(float(lambda1)-float(lambda2))))
	return angle*radius_of_earth