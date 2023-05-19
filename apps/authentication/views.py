# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import EmailMultiAlternatives, BadHeaderError
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.html import strip_tags
import uuid

from apps.account.models import UserAccount
from .forms import LoginForm, SignUpForm
from .models import Token


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                if UserAccount.objects.filter(username=username).exists():
                    msg = 'Wrong password!'
                else:
                    if UserAccount.objects.filter(email=username).exists():
                        msg = 'Please enter your username instead of email'
                    else:
                        msg = 'Account with this username does not exist.'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    return render(request, 'home/page-404.html')
#     msg = None
#     success = False

#     if request.method == "POST":
#         form = SignUpForm(request.POST)

#         if form.is_valid():
#             email = form.cleaned_data.get("email")
#             user_obj = UserAccount.objects.filter(email=email)
#             if len(user_obj) > 0:
#                 msg = 'This email is taken. Try with another email.'
                
#             else:
#                 form.save()
#                 username = form.cleaned_data.get("username")
#                 raw_password = form.cleaned_data.get("password1")

#                 user = authenticate(username=username, password=raw_password)
#                 login(request, user)
                
#                 msg = 'User created - please <a href="/login">login</a>.'
#                 success = True

#                 return redirect("home")
#         else:
#             msg = 'Form is not valid'

#     else:
#         form = SignUpForm()
#     return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})


def password_reset_request(request):
    if request.method == "POST":
        domain = request.headers['HOST']
        password_reset_form = PasswordResetForm(request.POST)

        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            users = UserAccount.objects.filter(Q(email=data))

            if users.exists():
                for user in users:
                    auth_token = str(uuid.uuid4())
                    Token.objects.create(user=user, auth_token=auth_token)

                    subject = "Password Reset Requested"
                    email_template_name = "accounts/password_reset_email.html"
                    c = {
                        "email": user.email,
                        "domain": domain,
                        "site_name": settings.SITE_NAME,
                        "user": user,
                        "auth_token": auth_token,
                        "protocol": settings.PROTOCOL,
                    }
                    html_content = render_to_string(email_template_name, c)
                    text_content = strip_tags(html_content)

                    try:
                        email = EmailMultiAlternatives(
                            subject,
                            text_content,
                            settings.EMAIL_HOST_USER,
                            [user.email]
                        )
                        email.attach_alternative(html_content, "text/html")
                        email.send()
                        return render(request, 'accounts/password_reset_email_sent.html')
                    except BadHeaderError:
                        return HttpResponse('Invalid Header Found!')
            else:
                messages.error(request, 'User with this email does not exist.')
                return redirect("password_reset")
        else:
            messages.error(request, 'Invalid credentials.') 
            return redirect("password_reset")

    password_reset_form = PasswordResetForm()
    context = {
        "password_reset_form": password_reset_form
    }
    return render(request, 'accounts/password_reset.html', context)


def confirm_password_reset(request, auth_token):
    if request.method == 'POST':
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        if not new_password1:
            messages.error(request, 'New password is required.')
            return redirect("password_reset_confirm")

        if not new_password2:
            messages.error(request, 'New password must be confirmed.')
            return redirect("password_reset_confirm")

        if new_password1 != new_password2:
            messages.error(request, 'Passwords did not match.')
            return redirect("password_reset_confirm")
        
        try:
            token = Token.objects.filter(auth_token=auth_token, password_changed=False).order_by('-id').first()
            
            user_obj = UserAccount.objects.filter(username=token.user.username).first()
            user_obj.set_password(new_password1)
            user_obj.save()
            
            token.password_changed = True
            token.save()
            
            return render(request, 'accounts/password_reset_done.html')
        except Exception:
            return render(request, 'accounts/password_reset_fail.html')

    return render(request, 'accounts/password_reset_confirm.html')


@login_required(login_url="login")
def change_password(request):
    try:
        if request.method == 'POST':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')

            if not old_password:
                messages.error(request, 'Enter your old password.')
                return redirect("change_password")

            if not new_password:
                messages.error(request, 'Enter new password.')
                return redirect("change_password")
            
            user = authenticate(username=request.user.username, password=old_password)
            
            if user is None:
                messages.error(request, 'Your old password is wrong!')
                return redirect("change_password")

            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            return render(request, 'accounts/change_password_success.html')

    except Exception:
        messages.error(request, 'Something went wrong! Try again.')
    
    return render(request, 'accounts/change_password.html')