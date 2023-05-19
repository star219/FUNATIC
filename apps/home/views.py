# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse

from .models import UploadedFile, Conditions
from .conversion import main


@login_required(login_url="/login/")
def index(request):
    objects = UploadedFile.objects.filter(user=request.user, converted=True).order_by('-id')
    return render(request, 'home/dashboard.html', {'objects': objects})


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="login")
def upload_pdf_view(request):
    if request.method == 'POST':
        width = int(request.POST.get('width'))
        height = int(request.POST.get('height'))
        color = int(request.POST.get('color'))
        pdf_file = request.FILES['pdf_file']

        if not pdf_file:
            messages.error(request, 'PDF file is required.')
            return redirect("upload_file")

        if not width:
            messages.error(request, 'Width is required.')
            return redirect("upload_file")

        if not height:
            messages.error(request, 'Height is required.')
            return redirect("upload_file")

        if not color:
            messages.error(request, 'Color is required.')
            return redirect("upload_file")

        if color < 3 or color > 8:
            messages.error(request, 'The range of color number is 3 to 8.')
            return redirect("upload_file")

        try:
            uploaded_file = UploadedFile.objects.create(
                user=request.user,
                width=width,
                height=height,
                color=color,
                file_name=pdf_file,
                file=pdf_file,
            )

            str_file = str(uploaded_file.file)
            slash_separated_array = str_file.split("/")
            sec_element = slash_separated_array[1]
            dot_separated_array = sec_element.split(".")
            uploaded_file.image_name = f'{dot_separated_array[0]}.bmp'
            uploaded_file.save()

            main(uploaded_file)

            uploaded_file.converted = True 
            uploaded_file.save()

            messages.success(request, 'Your file has been converted successfully.')
            protocol = settings.PROTOCOL
            domain = request.headers['HOST']
            context = {
                'protocol': protocol,
                'domain': domain,
                'up_file': uploaded_file.file,
                'image': uploaded_file.image
            }
            return render(request, 'home/display_image.html', context)

        except Exception:
            messages.error(request, 'Failed to convert your file!')
            return redirect("upload_file")

    return render(request, 'home/upload_pdf.html')


def terms_conditions_view(request):
    obj = Conditions.objects.all().order_by('-id').first()
    return render(request, 'home/terms_conditions.html', {'object': obj})