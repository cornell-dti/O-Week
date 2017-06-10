import json
import os
import csv

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.conf import settings

from wsgiref.util import FileWrapper

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import EventSerializer, CategorySerializer
from .models import EventDetail, Category
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
	try:
		event = EventDetail.objects.filter(pk = event_id)[0].images.name #assumes that it returns a correct one for now
		file_path = os.path.join(settings.MEDIA_ROOT, event)
		with open(file_path, 'rb') as fh:
			response = HttpResponse(fh.read(), status=status.HTTP_200_OK, content_type="image/jpg") #what if its not jpg
			response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
			return response
	except:
		return HttpResponse("",status = status.HTTP_400_BAD_REQUEST)
	
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
	else:
		form = BulkUploadForm()
	return render(request, 'bulk_add.html', {'form': form})
			
	
def add_event(request):
	if request.method == 'POST':
		form = EventDetailForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/thanks/')
	else:
		form = EventDetailForm()
	return render(request, 'add.html', {'form': form})

def add_category(request):
	if request.method == 'POST':
		form = CategoriesForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/thanks/')
	else:
		form = CategoriesForm()
	return render(request, 'addCategory.html', {'form': form})