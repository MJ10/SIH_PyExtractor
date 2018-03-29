from django.db import models
from datetime import date


# Create your models here.
DEPARTMENTS = (
	(0,'Department of ISRO'), (1,'Department of Agriculture'), (2,'Department of Space')
	)

class asset(models.Model):
	img_name = models.CharField(max_length=200)
	img_path = models.CharField(max_length=200)
	extracted_text = models.CharField(max_length=500)
	latitude = models.CharField(max_length=20)
	longitude = models.CharField(max_length=20)
	department = models.CharField(max_length=50)
	time = models.DateTimeField(auto_now_add=True)

	"""docstring for asset"""
	def __init__(self, arg):
		super(asset, self).__init__()
		self.arg = arg
		