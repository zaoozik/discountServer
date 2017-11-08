from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, HttpResponse
from cards.models import Card
from cards.serializers import CardSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

# Create your views here.
def listCards(request):
    cards = Card.objects.all()
    serializer = CardSerializer(cards, many=True)
    content = JSONRenderer().render(serializer.data)
    return HttpResponse(content, content_type="application/json")


def apiGetCard(request, org_id, card_code, salt):
    card = Card.objects.get( code=card_code, org=org_id)
    return HttpResponse(card.accumulation, status='200')

@csrf_exempt
def apiAddAccumToCard(request, org_id, card_code, salt):
    a = request.body
    card = Card.objects.get(code=card_code, org=org_id)
    card.accumulation += float(a)
    card.save()
    return HttpResponse(a)
