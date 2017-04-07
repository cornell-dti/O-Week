from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import EventDetail, Category

# Create your views here.

def index(request):
    return JsonResponse("Hello, world. You're at the flow index.", safe = False)

def feed(request, day, req_category = "none"):
	if req_category == "none":
		#returns eveything for storage on the app -> do we want to change this to a refreshing one
		event_set = EventDetail.objects.filter(start_date__date = str(day)) #because its a five day event
	else:
		cat_object = Category.objects.filter(category = req_category)
		event_set = EventDetail.objects.filter(start_date__date = str(day)).filter(category = cat_object)
	return JsonResponse(list(event_set.order_by('start_time', 'name')), safe = False)
	
def event_details(request, event_id):
	event = EventDetail.objects.filter(pk = event_id) #have to remove date generated, image will show up as a field with a url
	return JsonResponse(list(event), safe = False)

def categories(request):
	category_set = Category.objects.all().order_by('category')
	return JsonResponse(list(category_set), safe = False)
	
def add_event(request):
	return ""