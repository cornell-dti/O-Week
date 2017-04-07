from __future__ import unicode_literals

from django.db import models

""" """	
class Category(models.Model):
	category = models.CharField(max_length = 24, primary_key = True)
	description = models.TextField(max_length = 256)

""" """	
class Tag(models.Model):
	tag = models.CharField(max_length = 24, primary_key = True)
	description = models.TextField(max_length = 256)

""" """
class Organization(models.Model):
	# PK (id) automatically added
	name = models.CharField(max_length = 128)
	description = models.TextField(max_length = 1024, blank = True)
	owner = models.EmailField()
	contact = models.TextField() #todo
	image = models.ImageField(upload_to = "organizer_images") #todo
	links = models.SlugField()

""" """
class EventDetail(models.Model):
	# PK (id) automatically added
	name = models.CharField(max_length = 128)
	#organization = models.ForeignKey(Organization) #cascade?
	description = models.TextField(max_length = 1024, blank = True)
	location = models.TextField(max_length = 256)
	#price = models.DecimalField(decimal_places = 2)
	category = models.ForeignKey(Category) #cascade?
	generated = models.DateTimeField(auto_now = True)
	#thumbnail = model.ImageField(upload_to = "") #todo
	
	#Added post table alterations
	images = models.ImageField(upload_to = "event_images") 
	start_date = models.DateField()
	end_date = models.DateField()
	start_time = models.TimeField()
	end_time = models.TimeField()

""" """	
class EventTags(models.Model):
	#primary key is the set of columns {eventID,tag}
	eventID = models.ForeignKey(EventDetail, on_delete = models.CASCADE)
	tag = models.ForeignKey(Tag) #cascade?

#################### REMOVED #########################################

""" Removed. Not necessary to have a secondary table for event timings
because of the clustered nature of events. A second table with only this information
provides no new querying oppurtunities

class EventTime(models.Model):
	#Foriegn-Key -> many-to-one relationship. Multiple EventDetails
	#can be linked to the same event time, but since EventDetails are unique
	#this is effectively a one-to-one relationship.
	eventID = models.ForeignKey(EventDetail,
								primary_key = True,
								on_delete = models.CASCADE)
	start_date = models.DateField()
	end_date = models.DateField()
	start_time = models.TimeField()
	end_time = models.TimeField()
	
"""
	
""" Removed because O-events are small and
rarely have more than one accompanying media

class EventMedia(models.Model):
	eventID = models.ForeignKey(EventDetail,
								primary_key = True,
								on_delete = models.CASCADE)
	images = models.ImageField(upload_to = "")
	docs = models.FileField(upload_to = "")
"""