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
    path('api/keytable', views.KeyTableListCreate.as_view() ),
    path('admin/', admin.site.urls),
    #path('room_key', views.room_key),
    #url(r'admin/', admin.site.urls),
    #url(r'^api/', include(keytable_resource.urls)),
    #path('', include('api.urls')),
    path('show',views.show),
    path('test_insert', views.test_insert),
    path('test_delete', views.test_delete),
    path('test_update', views.test_update),
    path('test_get', views.test_get),
    path('test_get_rooms_count', views.test_get_rooms_count),
    path('test_get_apart_with_parking_and_study_room', views.test_get_apart_with_parking_and_study_room),
    path('insert', views.insert),
    path('delete', views.delete),
    path('update', views.update),
    path('test_apt_feature_insert', views.test_apt_feature_insert),
    path('test_apt_feature_delete', views.test_apt_feature_delete),
    path('apt_feature_insert', views.apt_feature_insert),
    path('apt_feature_delete', views.apt_feature_delete),
    path('get_rooms_count', views.get_rooms_count),
    path('get_apart_with_parking_and_study_room', views.get_apart_with_parking_and_study_room)
]
