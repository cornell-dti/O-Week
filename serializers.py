from rest_framework import serializers
from .models import EventDetail, Category

class EventSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EventDetail
        fields = ('pk', 'name', 'description', 'location', 'category', 'start_date', 'end_date', 'start_time', 'end_time')
		
class CategorySerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Category
        fields = ('category', 'description')