#-*- coding = utf-8 -*-
from django.urls import URLPattern, path
from django.contrib import admin
from django.conf.urls import url
from . import views
urlpatterns = [
    url('mainPage/',views.mainPage,name='mainPage'),
    url('upload/', views.uploadImage,name = 'uploadImage'),
]
