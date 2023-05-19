# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path
from apps.home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('upload-file/', views.upload_pdf_view, name='upload_file'),
    path('terms-conditions/', views.terms_conditions_view, name='terms_conditions'),
]
