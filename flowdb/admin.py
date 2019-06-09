# admin.py
# Arnav Ghosh
# 16th June 2017

from django.contrib import admin
from .models import Category, EventDetail, Tag, EventTags, Version
# Register your models here.

CAT = 'CAT'
EVE = 'EVE'

def add_mod_version(model, obj, change):
	version = Version()

	if model == CAT:
		version.model = CAT
		version.objID = obj.pk
	elif model == EVE:
		version.model = EVE
		version.objID = obj.pk

	if not change:
		version.operation = 'ADD'
	else:
		version.operation = 'MOD'
	version.save()

def delete_version(model, obj):
	version = Version()

	if model == CAT:
		version.model = CAT
	elif model == EVE:
		version.model = EVE

	version.objID = obj.pk
	version.operation = 'DEL'
	version.save()

class CategoryAdmin(admin.ModelAdmin):
	def save_model(self, request, obj, form, change):
		super(CategoryAdmin, self).save_model(request, obj, form, change)
		add_mod_version(CAT, obj, change)

	def delete_model(request, obj):
		obj.delete()  # hack
		delete_version(CAT, obj)

class EventDetailAdmin(admin.ModelAdmin):
	list_display = ('name', 'location', 'required')
	
	def save_model(self, request, obj, form, change):
		super(EventDetailAdmin, self).save_model(request, obj, form, change)
		add_mod_version(EVE, obj, change)

	def delete_model(request, obj):
		obj.delete()  # hack
		delete_version(EVE, obj)


admin.site.register(Category, CategoryAdmin)
admin.site.register(EventDetail, EventDetailAdmin)
admin.site.register(Tag)
admin.site.register(EventTags)
admin.site.register(Version)  # for now
