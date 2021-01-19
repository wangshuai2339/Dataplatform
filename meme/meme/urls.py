from django.conf.urls import include, url
from django.contrib import admin
urlpatterns = [

    url(r'^api/v1/', include('userrole.urls')),
    url(r'^api/v2/', include('memetest.urls')),
]
