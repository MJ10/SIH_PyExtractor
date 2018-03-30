from django.db import models
from datetime import date


# Create your models here.
DEPARTMENTS = (
	(0,'Department of ISRO'), (1,'Department of Agriculture'), (2,'Department of Space')
	)

CHOICE = (
	(0,'Kind'), (1,'capacity')
	)

class asset(models.Model):
	img_name = models.CharField(max_length=200)
	img_path = models.CharField(max_length=200)
	extracted_text = models.CharField(max_length=500)
	latitude = models.CharField(max_length=20)
	longitude = models.CharField(max_length=20)
	department = models.CharField(max_length=50)
	time = models.DateTimeField(auto_now_add=True)
	kind = models.CharField(max_length=50,blank=True,default=None, null=True)
	capacity = models.BigIntegerField(blank=True,default=0, null=True)
	"""docstring for asset"""
	# def __init__(self,img_name,img_path,extracted_text,latitude,longitude,department,time):
	# 	self.img_name = img_name
	# 	self.img_path = img_path
	# 	self.extracted_text = extracted_text
	# 	self.latitude = latitude
	# 	self.longitude = longitude
	# 	self.department = department
	# 	self.time = time
	def __str__(self):
		return self.img_name,self.img_path,self.extracted_text,self.latitude,self.longitude,self.department,self.time,self.kind,self.capacity
		