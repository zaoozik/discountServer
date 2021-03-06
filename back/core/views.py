
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Q
from rest_framework.request import Request

from users.models import UserCustom
import json
from datetime import datetime
from django.db import transaction
from .serializers import DiscountPlanSerializer, CashBoxesSerializer
from .models import DiscountPlan
from orgs.models import Org, CashBox, COUnit
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
        response['rules'] = json.loads(response['rules'])

        return JsonResponse(response, safe=False)

    if request.method == 'PUT':
        user = UserCustom.objects.get(user_id__exact=request.user.pk)
        dplan = DiscountPlan.objects.get(org_id__exact=user.org.pk)

        dplan_new_data = json.loads(request.body.decode())

        serializer_context = {
            'request': Request(request),
        }
        dplan_new_data['parameters'] = json.dumps(dplan_new_data['parameters'])
        dplan_new_data['rules'] = list(filter(lambda x: (x[0] is not None) and (x[1] is not None), dplan_new_data['rules']))
        dplan_new_data['rules'] = json.dumps(dplan_new_data['rules'])
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


@csrf_exempt
def rest_get_cashboxes(request):
    response = {}
    user = UserCustom.objects.get(user_id__exact=request.user.pk)
    org = user.org
    org.load_co()
    if request.method == 'GET':

        serializer_context = {
            'request': Request(request),
        }

        co_list = list()
        for co in org.co_unit:
            co.load_cashboxes()
            serializer = CashBoxesSerializer(co.cashboxes, many=True, context=serializer_context)
            co_list.append({'id': co.pk, 'name': co.name, 'address': co.address, 'cashboxes': serializer.data})

        response = co_list
        return JsonResponse(response, safe=False)

    if request.method == 'PUT':
        new_box_data = json.loads(request.body.decode())
        box = CashBox(**new_box_data)
        box.co_unit = COUnit.objects.get(id__exact=int(new_box_data['co_unit_id']))
        box.init_frontol_key()

        # serializer_context = {
        #     'request': Request(request),
        # }
        # serializer = CashBoxesSerializer(box, data=new_box_data)
        # if serializer.is_valid():
        #     serializer.save()
        #     response['status'] = 'success'
        #     response['message'] = 'Касса с кодом %s успешно сохранена!'
        #     return JsonResponse(response, safe=False)

        try:
            box.save()
            response['status'] = 'success'
            response['message'] = 'Касса успешно сохранена!'
            return JsonResponse(response, safe=False)
        except Exception as e:
            response['status'] = 'error'
            response['message'] = str(e)
            return JsonResponse(response, status=400)

    if request.method == 'DELETE':
        box_id = request.body.decode()

        try:
            box = CashBox.objects.get(pk=int(box_id))
        except Exception as e:
            response['status'] = 'error'
            response['message'] = str(e)
            return JsonResponse(response, status=400)

        try:
            box.delete()
            response['status'] = 'success'
            response['message'] = 'Касса удалена'
            return JsonResponse(response, safe=False)
        except Exception as e:
            response['status'] = 'error'
            response['message'] = str(e)
            return JsonResponse(response, status=400)

@csrf_exempt
def rest_get_counit(request):
    response = {}
    user = UserCustom.objects.get(user_id__exact=request.user.pk)
    org = user.org

    if request.method == 'PUT':
        new_counit_data = json.loads(request.body.decode())
        counit = COUnit(**new_counit_data)
        counit.org = org

        try:
            counit.save()
            response['status'] = 'success'
            response['message'] = 'Торговый объект успешно создан!'
            return JsonResponse(response, safe=False)
        except Exception as e:
            response['status'] = 'error'
            response['message'] = str(e)
            return JsonResponse(response, status=400)

    if request.method == 'DELETE':
        counit_id = request.body.decode()

        try:
            counit = COUnit.objects.get(pk=int(counit_id))
        except Exception as e:
            response['status'] = 'error'
            response['message'] = str(e)
            return JsonResponse(response, status=400)

        try:
            counit.delete()
            response['status'] = 'success'
            response['message'] = 'Торговый объект удален!'
            return JsonResponse(response, safe=False)
        except Exception as e:
            response['status'] = 'error'
            response['message'] = str(e)
            return JsonResponse(response, status=400)


@csrf_exempt
def rest_get_org(request):
    response = {}
    if request.method == 'GET':
        user = UserCustom.objects.get(user_id__exact=request.user.pk)
        response['name'] = user.org.name
        response['active_to'] = user.active_to

        return JsonResponse(response, safe=False)
