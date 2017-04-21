from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .models import EventDetail, Category, EventDetailForm, EventCategories

def index(request):
    return JsonResponse("Hello, world. You're at the flow index.", safe = False)

#need to alter to handle separate category table
def feed(request, day, req_category = "NONE"):
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
	return JsonResponse(list(event_set.order_by('start_time', 'name')), safe = False)
	
def event_details(request, event_id):
	event = EventDetail.objects.filter(pk = event_id) #have to remove date generated, image will show up as a field with a url
	return JsonResponse(list(event), safe = False)

def categories(request):
	category_set = Category.objects.all().order_by('category')
	return JsonResponse(list(category_set), safe = False)
	
def add_event(request):
	if request.method == 'POST':
		form = EventDetailForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/thanks/')
	else:
		form = EventDetailForm()
	return render(request, 'add.html', {'form': form})