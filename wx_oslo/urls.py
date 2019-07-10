#!/usr/bin/python
#-*- coding: UTF-8 -*- 


# @author Oslo
# @version 2019-07-10.

from django.conf.urls import include, url
from django.contrib import admin
from .views import *

urlpatterns = [
    url(r'^$',weixin),
]
