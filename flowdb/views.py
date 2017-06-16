import json
import os
import csv
import tempfile

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.conf import settings

from wsgiref.util import FileWrapper

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from boto.s3.connection import S3Connection
from boto.s3.key import Key

from .serializers import EventSerializer, CategorySerializer
from .models import EventDetail, Category, Version
from .forms import BulkUploadForm, EventDetailForm, CategoriesForm

def index(request):
    return JsonResponse("Hello, world. You're at the O-Week index.", safe = False)

@api_view(['GET'])
def feed(request, day, req_category = "NONE"):
    if request.method == 'GET':
        if req_category.lower() == "none":
            #returns eveything for storage on the app -> do we want to change this to a refreshing one
            event_set = EventDetail.objects.filter(start_date__day = str(day)) #because its a five day event
        else:
            cat_object = Category.objects.filter(category = req_category)
            corr_events = EventCategories.objects.filter(category = cat_object).values_list()
            event_set = EventDetail.objects.none()
            allDetails = EventDetail.objects.filter(start_date__day = str(day))
            for event in corr_events:
                spec_event = allDetails.filter(id = event)
                event_set.union(spec_event)
            
        serializer = EventSerializer(event_set, many = True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe = False)

@api_view(['GET'])
def event_details(request, event_id):
	try:
		event = EventDetail.objects.filter(pk = event_id)[0]
	except:
		return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST, safe = False)
	serializer = EventSerializer(event)
	return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe = False)

@api_view(['GET'])
def categories(request):
	category_set = Category.objects.all().order_by('category')
	serializer = CategorySerializer(category_set, many = True)
	return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe = False)

@api_view(['GET'])
def eventImage(request, event_id):
	event = EventDetail.objects.filter(pk = event_id)[0].images.name #assumes that it returns a correct one for now
	s3 = S3Connection(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
	s3bucket = s3.get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
	s3key = s3bucket.get_key(event)
	fh = tempfile.TemporaryFile()
	s3file = s3key.get_contents_to_file(fh)
	response = HttpResponse(fh.read(), status=status.HTTP_200_OK, content_type="image/jpg") #what if its not jpg
	response['Content-Disposition'] = 'inline; filename=' + event
	return response

def bulk_add(request):
	if request.method == 'POST':
		form = BulkUploadForm(request.POST, request.FILES)
		if form.is_valid():
			csvFile = form.cleaned_data['csvFile']
			dataReader = csv.reader(csvFile, delimiter=',', quotechar='"')
			for row in dataReader:
				event = EventDetail()
				event.name = row[0]
				event.description = row[1]
				event.location = row[2]
				cat_object = Category.objects.filter(category = row[3])[0]
				event.category = cat_object
				event.start_date = row[4]
				event.end_date = row[5]
				event.start_time = row[6]
				event.end_time = row[7]
				event.required = bool(row[8])
				event.save()

				event_version = Version()
				event_version.model = 'EVE'
				event_version.objID = event.pk
				event_version.operation = 'ADD'
				event_version.save()
	else:
		form = BulkUploadForm()
	return render(request, 'bulk_add.html', {'form': form})

def versionedFeed(request, version):
	catDict, eventDict = versionChanges(version)
	changedCats = Category.objects.filter(pk__in=catDict['CHANGED'])
	changedEvents = EventDetail.objects.filter(pk__in=eventDict['CHANGED'])
	eventserializer = EventSerializer(changedEvents, many = True)
	catserializer = CategorySerializer(changedCats, many = True)
	return JsonResponse({
							'events'	: {
											'changed': eventserializer.data,
											'deleted': eventDict['DELETED']
									  	  },
							'categories': {
											'changed': catserializer.data,
											'deleted': catDict['DELETED']
										  },
							'version' 	: Version.objects.latest('pk').pk
						}
						, status=status.HTTP_200_OK, safe = False)

def versionChanges(version):
	allChanges = Version.objects.filter(pk__gt = version).order_by('pk')
	catDict = {'CHANGED':[], 'DELETED':[]}
	eventDict = {'CHANGED':[], 'DELETED':[]}
	for change in allChanges:
		op = change.operation
		if change.model == 'CAT' and op == 'DEL':
			catDict = dictDeleted(catDict, change.objID)
		elif change.model == 'CAT' and (op == 'MOD' or op == 'ADD'):
			catDict = dictChanges(catDict, change.objID)
		elif change.model == 'EVE' and op == 'DEL':
			eventDict = dictDeleted(eventDict, change.objID)
		elif change.model == 'EVE' and (op == 'MOD' or op == 'ADD'):
			eventDict = dictChanges(eventDict, change.objID)
	return catDict, eventDict

def dictChanges(alterDict, objID):
	if objID in alterDict['CHANGED']:
		pass
	else:
		alterDict['CHANGED'] = alterDict['CHANGED'] + [objID]
	return alterDict

def dictDeleted(alterDict, objID):
	if objID in alterDict['CHANGED']:
		alterDict['CHANGED'].remove(objID)
	else:
		pass
	alterDict['DELETED'] = alterDict['DELETED'] + [objID]
	return alterDict