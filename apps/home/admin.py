# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import UploadedFile, Conditions


class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('user', 'file_name', 'image_name', 'width', 'height', 'color', 'converted')
    list_display_links = ('user', 'file_name', 'image_name', 'width', 'height')
    list_filter = ('converted',)
    ordering = ['-id']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'file_name', 'image_name']

admin.site.register(UploadedFile, UploadedFileAdmin)

admin.site.register(Conditions)
