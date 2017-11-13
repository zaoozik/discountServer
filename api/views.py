from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, HttpResponse
from cards.models import Card
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
@csrf_exempt
def apiGetCard(request, org_id, card_code, salt):
    if request.method == 'POST':
        data = request.POST
        if ('username' in data) and ('password' in data):
            user = authenticate(username=data['username'], password=data['password'])
            if user is not None:
                if user.is_active:
                    try:
                        card = Card.objects.get(code=card_code, org=org_id)
                        return HttpResponse(card.bonus, status='200')
                    except ObjectDoesNotExist as e:
                        return HttpResponse(status='404')
                else:
                    return HttpResponse(status='503')
            else:
                return HttpResponse(status='503')
        else:
            return HttpResponse(status='503')


@csrf_exempt
def apiAddAccumToCard(request, org_id, card_code, salt):
    if request.method == 'POST':
        data = request.POST
        if ('username' in data) and ('password' in data):
            user = authenticate(username=data['username'], password=data['password'])
            if user is not None:
                if user.is_active:
                    try:
                        if 'value' in data:
                            card = Card.objects.get(code=card_code, org=org_id)
                            card.accumulation += float(data['value'])
                            card.save()
                            return HttpResponse(data['value'])
                        else:
                            return HttpResponse(status='404')
                    except ObjectDoesNotExist as e:
                        return HttpResponse(status='404')
                else:
                    return HttpResponse(status='503')
            else:
                return HttpResponse(status='503')
        else:
            return HttpResponse(status='503')


@csrf_exempt
def apiRemAccumToCard(request, org_id, card_code, salt):
    if request.method == 'POST':
        data = request.POST
        if ('username' in data) and ('password' in data):
            user = authenticate(username=data['username'], password=data['password'])
            if user is not None:
                if user.is_active:
                    try:
                        if 'value' in data:
                            card = Card.objects.get(code=card_code, org=org_id)
                            card.accumulation -= float(data['value'])
                            card.save()
                            return HttpResponse(data['value'])
                        else:
                            return HttpResponse(status='404')
                    except ObjectDoesNotExist as e:
                        return HttpResponse(status='404')
                else:
                    return HttpResponse(status='503')
            else:
                return HttpResponse(status='503')
        else:
            return HttpResponse(status='503')

@csrf_exempt
def apiRemBonusToCard(request, org_id, card_code, salt):
    if request.method == 'POST':
        data = request.POST
        if ('username' in data) and ('password' in data):
            user = authenticate(username=data['username'], password=data['password'])
            if user is not None:
                if user.is_active:
                    try:
                        if 'value' in data:
                            card = Card.objects.get(code=card_code, org=org_id)
                            card.bonus -= float(data['value'])
                            card.save()
                            return HttpResponse(data['value'])
                        else:
                            return HttpResponse(status='404')
                    except ObjectDoesNotExist as e:
                        return HttpResponse(status='404')
                else:
                    return HttpResponse(status='503')
            else:
                return HttpResponse(status='503')
        else:
            return HttpResponse(status='503')