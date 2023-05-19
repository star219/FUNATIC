# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.conf import settings
from django.db import models
from ckeditor.fields import RichTextField


User = settings.AUTH_USER_MODEL 

class UploadedFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    width = models.IntegerField()
    height = models.IntegerField()
    color = models.IntegerField()
    file_name = models.CharField(max_length=200)
    file = models.FileField(upload_to="files/")
    image_name = models.CharField(max_length=210, blank=True, null=True)
    image = models.ImageField(upload_to="converted_files/", blank=True, null=True)
    converted = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Uploaded PDF Files'

    def __str__(self):
        return f'{self.file_name} -> {self.image_name}'


class Conditions(models.Model):
    description = RichTextField()

    class Meta:
        verbose_name_plural = 'Terms and Conditions'

    def __str__(self):
        return str(self.id)