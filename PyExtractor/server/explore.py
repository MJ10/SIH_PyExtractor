from django.shortcuts import render
from server import models
from server.models import asset, Account
from server.forms import QueryForm
import math
from server import views
from django.db.models import Q

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
	authentication_result = views.authentication_check(request, [Account.ACCOUNT_ADMIN])
	if authentication_result is not None:
		return authentication_result
	template_data = parse_session(
		request,
		{'form_button':'Query'}
	)
	if request.method == 'POST':
		form = QueryForm(request.POST)
		if form.is_valid():
			# Query to find images in that range
			desired_id = find_images(form.cleaned_data['department'],form.cleaned_data['latitude'],form.cleaned_data['longitude'], form.cleaned_data['distance'], form.cleaned_data['year'], form.cleaned_data['input_text_type'], form.cleaned_data['input_text_capacity'])
			print(desired_id)
			# for id_i in desired_id:
			# #asset.objects.filter(id=id_i))
			# 	template_data['query']=asset.objects.filter(
			# 		Q(id=id_i)
			# 	)
			template_data['query']=asset.objects.filter(pk__in=desired_id)
			print(template_data['query'])
	else:
		form = QueryForm()
	template_data['form'] = form
	return render(request, 'explore.html', template_data)


# Function to find images having the distance which user wants
def find_images(department,latitude,longitude, distance, year, input_text_type, input_text_capacity):
	desired_id = []
	print(department,latitude,longitude,distance,year,input_text_type,input_text_capacity)
	phi1 = toRadians(latitude)
	lambda1 = toRadians(longitude)
	print(phi1,lambda1)

	for asseti in asset.objects.all():
		phi2 = toRadians(asseti.latitude)
		lambda2 = toRadians(asseti.longitude)
		# If any one is NULL
		if(phi2 == -1 or lambda2 == -1):
			print("Do nothing")
		else:
			got_distance = getDistance(phi1,phi2,lambda1,lambda2,distance)
			print(got_distance)
			if input_text_capacity == '' and input_text_type == '':
				if got_distance < float(distance) and int(asseti.department) == int(department):
					print(asseti.img_name)
					desired_id.append(asseti.id)
			elif input_text_capacity == '':
				if got_distance < float(distance) and int(asseti.department) == int(department) and asseti.kind == str(input_text_type):
					print(asseti.img_name)
					desired_id.append(asseti.id)
			elif input_text_type == '':
				if got_distance < float(distance) and int(asseti.department) == int(department) and int(asseti.capacity) <= int(input_text_capacity):
					print(asseti.img_name)
					desired_id.append(asseti.id)
			else:
				if got_distance < float(distance) and int(asseti.department) == int(department) and int(asseti.capacity) <= int(input_text_capacity) and asseti.kind == str(input_text_type):
					print(asseti.img_name)
					desired_id.append(asseti.id)

	return desired_id



# Convert the latitude and longitude to Radians
def toRadians(input):
	if input == None:
		return -1
	else:
		return 0.0174533*float(input)

# Get distance between the two points
def getDistance(phi1,phi2,lambda1,lambda2,radius):
	angle = math.acos(math.sin(float(phi1))*math.sin(float(phi2)) + math.cos(float(phi1))*math.cos(float(phi2))*math.cos(abs(float(lambda1)-float(lambda2))))
	return angle*radius_of_earth