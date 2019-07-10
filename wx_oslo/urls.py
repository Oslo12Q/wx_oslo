from django.conf.urls import include, url
from django.contrib import admin
from .views import *

urlpatterns = [
    url(r'^$',weixin),
    url(r'^del_tags/',del_tags),
    url(r'^admin/', include(admin.site.urls)),
]
