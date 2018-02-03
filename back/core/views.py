from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Q
from rest_framework.request import Request

from cards.models import Card
from django.contrib.auth.decorators import login_required
from django.template import loader
from users.models import UserCustom
import json
from datetime import datetime
from django.db import transaction
from .serializers import DiscountPlanSerializer
from .models import DiscountPlan
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

# Create your views here.


# REST API VIEWS
@csrf_exempt
def rest_get_discount_plan(request):
    response = {}
    if request.method == 'GET':
        user = UserCustom.objects.get(user_id__exact=request.user.pk)
        dplan = DiscountPlan.objects.get(org_id__exact=user.org.pk)

        serializer_context = {
            'request': Request(request),
        }

        serializer = DiscountPlanSerializer(dplan, many=False, context=serializer_context)
        response = serializer.data

        return JsonResponse(response, safe=False)

    if request.method == 'PUT':
        user = UserCustom.objects.get(user_id__exact=request.user.pk)
        dplan = DiscountPlan.objects.get(org_id__exact=user.org.pk)

        dplan_new_data = json.loads(request.body.decode())

        serializer_context = {
            'request': Request(request),
        }
        dplan_new_data['parameters'] = json.dumps(dplan_new_data['parameters'])
        dplan_new_data['org'] = user.org.pk
        serializer = DiscountPlanSerializer(dplan, data=dplan_new_data)
        if serializer.is_valid():
            serializer.save()
            response['status'] = 'success'
            response['message'] = 'Настройки успешно сохранены!'
            return JsonResponse(response, safe=False)
        response['status'] = 'error'
        response['message'] = str(serializer.errors)
        return JsonResponse(response, status=400)




