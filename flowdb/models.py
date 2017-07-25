# models.py
# Arnav Ghosh
# 16th June 2017

from __future__ import unicode_literals

from django.db import models

""" """	
class Category(models.Model):
	category = models.CharField(max_length = 24)
	description = models.TextField(max_length = 256)
	
	def __str__(self):
		return self.category

	class Meta:
		verbose_name_plural = "Categories"

""" """	
class Tag(models.Model):
	tag = models.CharField(max_length = 24, primary_key = True)
	description = models.TextField(max_length = 256)
	
	def __str__(self):
		return self.tag

	class Meta:
		verbose_name_plural = "Tags"

""" """
class EventDetail(models.Model):
	# PK (id) automatically added
	name = models.CharField(max_length = 512)
	description = models.TextField(max_length = 5096, blank = True)
	location = models.TextField(max_length = 512)
	latitute = models.DecimalField(max_digits = 10, decimal_places = 7)
	longitude = models.DecimalField(max_digits = 10, decimal_places = 7)
	category = models.ForeignKey(Category) #cascade?
	generated = models.DateTimeField(auto_now = True)
	required = models.BooleanField(default = False)
	
	#Added post table alterations
	images = models.ImageField(upload_to = "event_images", blank = True) 
	start_date = models.DateField()
	end_date = models.DateField()
	start_time = models.TimeField()
	end_time = models.TimeField()
	
	#def __str__(self):
	#	return self.name + " (" + self.start_date.strftime('%m/%d/%Y') + ")"

	class Meta:
		verbose_name_plural = "Event Details"

""" """	
class EventTags(models.Model):
	#primary key is the set of columns {eventID,tag}
	eventID = models.ForeignKey(EventDetail, on_delete = models.CASCADE)
	tag = models.ForeignKey(Tag, on_delete = models.CASCADE)

	def __str__(self):
		return eventID.name + "," + tag.tag

	class Meta:
		verbose_name_plural = "Event Tags"

""" """
class Version(models.Model):	
	MODEL_CHOICES = (
		('CAT', 'CATEGORY'),
		('EVE', 'EVENTDETAIL')
	)

	OPERATION_CHOICES = (
		('ADD', 'ADD'),
		('MOD', 'MODIFY'),
		('DEL', 'DELETED')
	)

	model = models.CharField(max_length = 3, choices = MODEL_CHOICES, editable = False)
	objID = models.IntegerField(editable = False)
	operation = models.CharField(max_length = 3, choices = OPERATION_CHOICES, editable = False)

	def __str__(self):
		return self.model + "," + str(self.objID) + "," + self.operation