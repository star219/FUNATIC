# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.conf import settings 
from django.conf.urls.static import static 
from django.contrib import admin
from django.urls import path, include, re_path  # add this
from apps.home.views import pages

admin.site.site_header = settings.SITE_NAME
admin.site.site_title = settings.SITE_NAME
admin.site.index_title = "Administration area"


urlpatterns = [
    path('control/', admin.site.urls),          # Django admin route
    path("", include("apps.authentication.urls")), # Auth routes - login / register
    path("", include("apps.home.urls")),           # UI Kits Html files
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        re_path(r'^.*', pages, name='pages'),     # Matches any html file
    ]

if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^.*', pages, name='pages'),     
    ]