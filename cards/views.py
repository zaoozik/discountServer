from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, HttpResponse
from cards.models import Card
from cards.serializers import CardSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.contrib.auth.decorators import login_required
from django.template import loader

# Create your views here.


@login_required(login_url='../login/')
def listCards(request):
    cards = Card.objects.order_by('code')
    template = loader.get_template('list_cards.html')
    response = {"cards": cards}
    return HttpResponse(template.render(response, request))




