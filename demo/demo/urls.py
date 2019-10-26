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
from django.urls import path
from demosite import views
from django.urls import path, include

urlpatterns = [
    #path('', urls),#
    # path('', include('demosite.urls')),
    # path('api/keytable', views.KeyTableListCreate.as_view() ),
    path('admin/', admin.site.urls),
    path('room_key', views.room_key),
    path('show',views.show),
    path('test_insert', views.test_insert),
    path('test_delete', views.test_delete),
    path('test_update', views.test_update),
    path('test_post', views.test_get),
    path('insert', views.insert),
    path('delete', views.delete)
]
