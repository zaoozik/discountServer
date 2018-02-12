import json
from django.shortcuts import render

from queues.serializers import TaskSerializer
from .models import Transaction
from django.contrib.auth.decorators import login_required
from users.models import UserCustom
from queues.models import Task
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.template import loader
from django.db.models import Q
from rest_framework.request import Request


# Create your views here.
@login_required
def listQueue(request):
    if request.method == "GET":
        response = {}
        template = loader.get_template('queue.html')
        return HttpResponse(template.render(response, request))

    if request.method == "POST":
        user = UserCustom.objects.get(user_id__exact=request.user.pk)
        q = Q(org_id__exact=user.org.pk)
        data = None
        selection_parameters = None
        post = request.POST
        if "cmd" in post:
            if post["cmd"] == "update":
                if "data" in post:
                    data = json.loads(post["data"])
                if "selection_parameters" in post:
                    selection_parameters = json.loads(post["selection_parameters"])
                if selection_parameters is not None:
                    a =1
                tasks = Task.objects.filter(q)
                total = len(tasks)
                if data["count"] > total:
                    data["count"] = total
                tasks = tasks.all()[
                        data["start"]:data["start"] + data["count"]]
                resp_tasks = []
                for task in tasks:
                    resp_tasks.append(
                        {
                            "execution_date": task.execution_date.strftime('%Y-%m-%d / %H:%M'),
                            "queue_date": task.queue_date.strftime('%Y-%m-%d / %H:%M'),
                            "operation": task.get_operation(),
                            "card": task.card.code,
                            "sum": task.transaction.sum,
                            "shop": task.transaction.shop,
                            "workplace": task.transaction.workplace,
                            "session": task.transaction.session,
                            "doc_number": task.transaction.doc_number
                        }
                    )

                response = {"result": "ok", "data": resp_tasks, "total": total}
                return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def rest_task_list(request):
    if request.method == "GET":
        response = {}
        user = UserCustom.objects.get(user_id__exact=request.user.pk)

        task = Task.objects.filter(org_id__exact=user.org.pk)[:100]

        serializer_context = {
            'request': Request(request),
        }

        serializer = TaskSerializer(task, many=True, context=serializer_context)
        response = serializer.data
        return JsonResponse(response, safe=False)
