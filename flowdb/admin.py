from django.contrib import admin
from .models import Category, EventDetail, Tag, EventTags, EventCategories
# Register your models here.

admin.site.register(Category)
admin.site.register(EventDetail)
admin.site.register(Tag)
admin.site.register(EventTags)
admin.site.register(EventCategories)