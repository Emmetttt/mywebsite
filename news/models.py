from django.db import models

# Create your models here.
class News(models.Model):
	headline = models.CharField(max_length=500)
	url = models.CharField(max_length=500)
	tag = models.CharField(max_length=500)
	source = models.CharField(max_length=500)