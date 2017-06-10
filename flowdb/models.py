from __future__ import unicode_literals

from django.db import models

""" """	
class Category(models.Model):
	category = models.CharField(max_length = 24, primary_key = True)
	description = models.TextField(max_length = 256)
	
	def __str__(self):
		return self.category

""" """	
class Tag(models.Model):
	tag = models.CharField(max_length = 24, primary_key = True)
	description = models.TextField(max_length = 256)
	
	def __str__(self):
		return self.tag

""" """
class EventDetail(models.Model):
	# PK (id) automatically added
	name = models.CharField(max_length = 128)
	description = models.TextField(max_length = 1024, blank = True)
	location = models.TextField(max_length = 256)
	category = models.ForeignKey(Category) #cascade?
	generated = models.DateTimeField(auto_now = True)
	required = models.BooleanField(default = False)
	
	#Added post table alterations
	images = models.ImageField(upload_to = "event_images") 
	start_date = models.DateField()
	end_date = models.DateField()
	start_time = models.TimeField()
	end_time = models.TimeField()
	
	def __str__(self):
		return self.name + " (" + self.start_date.strftime('%m/%d/%Y') + ")"

""" """	
class EventTags(models.Model):
	#primary key is the set of columns {eventID,tag}
	eventID = models.ForeignKey(EventDetail, on_delete = models.CASCADE)
	tag = models.ForeignKey(Tag, on_delete = models.CASCADE)

	def __str__(self):
		return eventID.name + "," + tag.tag

################################ REMOVED #########################################

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

""" """
class Organization(models.Model):
	# PK (id) automatically added
	name = models.CharField(max_length = 128)
	description = models.TextField(max_length = 1024, blank = True)
	owner = models.EmailField()
	contact = models.TextField() #todo
	image = models.ImageField(upload_to = "organizer_images") #todo
	links = models.SlugField()
	
	def __str__(self):
		return self.names

class EventCategories(models.Model):
	#primary key is the set of columns {eventID,category}
	eventID = models.ForeignKey(EventDetail, on_delete = models.CASCADE) #is this ID?
	category = models.ForeignKey(Category, on_delete = models.CASCADE)

	def __str__(self):
		return eventID.name + "," + category.category

"""