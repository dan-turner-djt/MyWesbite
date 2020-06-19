from django.conf import settings
from django.db import models
from django.utils import timezone
from django import forms


class Post (models.Model):
	author = models.ForeignKey (settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	title = models.CharField (max_length=200)
	text = models.TextField()
	created_date = models.DateTimeField (default=timezone.now)
	published_date = models.DateTimeField (blank=True, null=True)

	def publish (self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.title



class CVEntry (models.Model):
	title = models.CharField (max_length=200)
	location = models.CharField(max_length=200, blank=True)
	text = models.TextField(blank=True)
	start_date = models.CharField (max_length=200, blank=True)
	end_date = models.CharField (max_length=200, blank=True)
	created_date = models.DateTimeField (default=timezone.now)
	published_date = models.DateTimeField (blank=True, null=True)
	section = models.CharField (max_length=200)

	def publish (self):
		self.published_date = timezone.now()
		self.save()

	def __str__(self):
		return self.title
	

