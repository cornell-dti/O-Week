# urls.py
# Arnav Ghosh
# 16th June 2017

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^feed/(?P<day>[1-9]|[12][0-9]|3[01])/$', views.feed, name='feed by date'),
    url(r'^feed/(?P<day>[1-9]|[12][0-9]|3[01])/(?P<req_category>[a-zA-z]+)/$', views.feed,
        name='feed with category'),
    url(r'^version/(?P<version>[0-9]+)$', views.versionedFeed, name='update version'),
    url(r'^event/(?P<event_id>[0-9]+)/$', views.event_details, name='event details'),
    url(r'^event/(?P<event_id>[0-9]+)/image$', views.eventImage, name='event image'),
    url(r'^categories/$', views.categories, name='categories'),
    url(r'^bulk_add_event/$', views.bulk_add, name='bulk add'),
    url(r'^bulk_add_categories/$', views.upload_categories, name='bulk categories'),
    url(r'^bulk_image/$', views.image_for_all, name='bulk image upload'),
    url(r'^dates/$', views.dates, name='dates in orientation'),
    url(r'^resources/$', views.resources, name='name and description of resources')
]
