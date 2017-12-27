from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.


def list_service(request):
    template = loader.get_template('list_service.html')

    return HttpResponse(template.render({}, request))
