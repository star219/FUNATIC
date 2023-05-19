# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.conf import settings
from django.db import models


User = settings.AUTH_USER_MODEL 

class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=40)
    password_changed = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Tokens'

    def __str__(self):
        if self.user.first_name:
            return f"self.user.first_name self.user.last_name"
        return f"self.user.username"
 