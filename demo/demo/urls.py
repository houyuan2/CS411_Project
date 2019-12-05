"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from demosite import views

from django.conf.urls import url, include
#from api.resources import KeyTableResource

#keytable_resource = KeyTableResource()


urlpatterns = [
    # path('api/keytable', views.KeyTableListCreate.as_view() ),
    path('admin/', admin.site.urls),
    #path('room_key', views.room_key),
    #url(r'admin/', admin.site.urls),
    #url(r'^api/', include(keytable_resource.urls)),
    #path('', include('api.urls')),
    path('show',views.show),
    path('search', views.search),
    path('oldfiltershow', views.oldfiltershow),
    path('keytable_insert', views.keytable_insert),
    path('keytable_delete', views.keytable_delete),
    path('keytable_update', views.keytable_update),
    path('apartfeature_insert', views.apartfeature_insert),
    path('apartfeature_delete', views.apartfeature_delete),
    path('get_rooms_count', views.get_rooms_count),
    path('get_apart_with_parking_and_study_room', views.get_apart_with_parking_and_study_room),
    path('roomfeature_insert', views.roomfeature_insert),
    path('roomfeature_delete', views.roomfeature_delete),
    path('distancetable_insert', views.distancetable_insert),
    path('distancetable_delete', views.distancetable_delete),
    path('ratingtable_insert', views.ratingtable_insert),
    path('ratingtable_delete', views.ratingtable_delete),
    path('peoplerating_insert', views.peoplerating_insert),
    path('peoplerating_delete', views.peoplerating_delete),
    path('AF1Distance', views.AF1Distance),
    path('update_nearby', views.update_nearby),
    path('new_show', views.new_show),
    path('test', views.test),
    path('selectforyou', views.selectforyou),
    path('advance_filter', views.advance_filter),
    path('similar_apart', views.similar_apart),
    path('apartfeature_update', views.apartfeature_update)
]