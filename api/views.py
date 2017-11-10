from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, HttpResponse
from cards.models import Card


# Create your views here.
def apiGetCard(request, org_id, card_code, salt):
    if request.method == 'GET':
        try:
            card = Card.objects.get( code=card_code, org=org_id)
            return HttpResponse(card.accumulation, status='200')
        except ObjectDoesNotExist as e:
            return HttpResponse(status='404')

@csrf_exempt
def apiAddAccumToCard(request, org_id, card_code, salt):
    a = request.body
    card = Card.objects.get(code=card_code, org=org_id)
    card.accumulation += float(a)
    card.save()
    return HttpResponse(a)

@csrf_exempt
def apiRemAccumToCard(request, org_id, card_code, salt):
    if request.method == 'POST':
        try:
            a = request.body
            card = Card.objects.get(code=card_code, org=org_id)
            card.accumulation -= float(a)
            card.save()
            return HttpResponse(a)
        except ObjectDoesNotExist as e:
            return HttpResponse(status='404')