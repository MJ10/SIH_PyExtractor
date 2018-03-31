from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
DEPARTMENTS = (
	(10,'Department of ISRO'), (20,'Department of Agriculture'), (30,'Department of Defence'),
	(40,'Department of Telecommunications'), (50,'Department of IT')
	)

CHOICE = (
	(0,'Kind'), (1,'capacity')
	)

# class Profile(models.Model):
# 	department = models.CharField(max_length=100)

class Account(models.Model):
	ACCOUNT_ISRO = 10
	ACCOUNT_AGRI = 20
	ACCOUNT_DEF = 30
	ACCOUNT_TELE = 40
	ACCOUNT_IT = 50
	ACCOUNT_ADMIN = 60
	ACCOUNT_TYPES = (
		(ACCOUNT_ISRO, "ISRO"),
		(ACCOUNT_AGRI, "Agriculture"),
		(ACCOUNT_DEF, "Defence"),
		(ACCOUNT_TELE, "Telecommunications"),
		(ACCOUNT_IT, "IT"),
		(ACCOUNT_ADMIN,"Admin")
	)
	EMPLOYEE_TYPES = (
		(ACCOUNT_ISRO, "ISRO"),
		(ACCOUNT_AGRI, "Agriculture"),
		(ACCOUNT_DEF, "Defence"),
		(ACCOUNT_TELE, "Telecommunications"),
		(ACCOUNT_IT, "IT"),
		(ACCOUNT_ADMIN, "Admin")
	)

	@staticmethod
	def to_name(key):
		for item in Account.ACCOUNT_TYPES:
			if item[0]==key:
				return item[1]
		return "None"

	@staticmethod
	def to_value(key):
		key = key.lower()
		for item in Account.ACCOUNT_TYPES:
			if item[1].lower() == key:
				return item[0]
		return 0

	role = models.IntegerField(default=0, choices=ACCOUNT_TYPES)
	user = models.OneToOneField(User, on_delete=models.CASCADE)


	class Admin:
		list_display = (
			'role',
			'user',
		)


class asset(models.Model):
	img_name = models.CharField(max_length=200)
	img_path = models.CharField(max_length=200)
	extracted_text = models.CharField(null=True,max_length=500)
	latitude = models.CharField(null=True,max_length=20)
	longitude = models.CharField(null=True,max_length=20)
	department = models.CharField(max_length=50)
	time = models.DateTimeField(auto_now_add=False)

	kind = models.CharField(max_length=50,blank=True,default=None, null=True)

	capacity = models.CharField(default=0, null=True, max_length=100)
	owner = models.CharField(null=True,max_length=50)
	"""docstring for asset"""
	# def __init__(self,img_name,img_path,extracted_text,latitude,longitude,department,time):
	# 	self.img_name = img_name
	# 	self.img_path = img_path
	# 	self.extracted_text = extracted_text
	# 	self.latitude = latitude
	# 	self.longitude = longitude
	# 	self.department = department
	# 	self.time = time
#	def __str__(self):
#		return self.img_name,self.img_path,self.extracted_text,self.latitude,self.longitude,self.department,self.time,self.kind,self.capacity, self.owner
	
	def __str__(self):
		return '{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}'.format(self.img_name,self.img_path,self.extracted_text,self.latitude,self.longitude,self.department,self.time,self.kind,self.capacity, self.owner)