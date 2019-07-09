from django.conf.urls import include, url
from django.contrib import admin
from .views import *

urlpatterns = [
    url(r'^$',weixin),
    url(r'^admin/', include(admin.site.urls)),
]
