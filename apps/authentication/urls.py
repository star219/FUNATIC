# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import (
    login_view, password_reset_request, change_password, register_user,
    confirm_password_reset
)

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('change-password/', change_password, name="change_password"),
    path('password-reset/', password_reset_request, name="password_reset"),
    path('reset/<auth_token>/', confirm_password_reset, name="password_reset_confirm"),
]
