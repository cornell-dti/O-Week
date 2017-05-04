from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
import json, os

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import EventSerializer, CategorySerializer
from .models import EventDetail, Category, EventDetailForm, EventCategories
from wsgiref.util import FileWrapper
from django.conf import settings


def index(request):
    return JsonResponse("Hello, world. You're at the flow index.", safe = False)

@api_view(['GET'])
def feed(request, day, req_category = "NONE"):
    if request.method == 'GET':
        if req_category.lower() == "none":
            #returns eveything for storage on the app -> do we want to change this to a refreshing one
            event_set = EventDetail.objects.filter(start_date__day = str(day)) #because its a five day event
        else:
            cat_object = Category.objects.filter(category = req_category)
            corr_events = EventCategories.filter(category = cat_object).values_list()
            event_set = EventDetail.objects.none()
            for event in corr_events:
                spec_event = EventDetail.objects.filter(start_date__day = str(day)).filter(id = event)
                event_set.union(spec_event)
            
        serializer = EventSerializer(event_set, many = True)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe = False)

@api_view(['GET'])
def event_details(request, event_id):
	event = EventDetail.objects.filter(pk = event_id) #have to remove date generated, image will show up as a field with a url
	serializer = EventSerializer(event, many = True) #prevent errors due to None for now
	return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe = False)

@api_view(['GET'])
def categories(request):
	category_set = Category.objects.all().order_by('category')
	serializer = CategorySerializer(category_set, many = True)
	return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe = False)

@api_view(['GET'])
def eventImage(request, event_id):
	event = EventDetail.objects.filter(pk = event_id)[0].images.name #assumes that it returns a correct one for now
	file_path = os.path.join(settings.MEDIA_ROOT, event)
	if os.path.exists(file_path):
		with open(file_path, 'rb') as fh:
			response = HttpResponse(fh.read(), content_type="image/jpg")
			response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
			return response
	else:
		raise HttpResponse("")
	
def add_event(request):
	if request.method == 'POST':
		form = EventDetailForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/thanks/')
	else:
		form = EventDetailForm()
	return render(request, 'add.html', {'form': form})