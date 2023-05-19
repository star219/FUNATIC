# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from .models import Token


class TokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'password_changed')
    list_display_links = ('user',)
    list_filter = ('password_changed',)
    ordering = ['-id']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'auth_token']

admin.site.register(Token, TokenAdmin)