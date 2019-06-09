# serializers.py
# Arnav Ghosh
# 16th June 2017

from rest_framework import serializers
from .models import EventDetail, Category, Resource, Date


class DateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Date
        fields = 'date'


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ('name', 'link')


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventDetail
        fields = (
            'pk', 'name', 'description', 'additional', 'location', 'latitude', 'longitude',
            'category', 'start_date', 'end_date', 'start_time', 'end_time', 'required',
            'category_required')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('pk', 'category', 'description')
