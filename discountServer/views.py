import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(request, 'main.html')


def signIn(request):
    response={}
    if request.method == "GET":
        return render(request, 'login.html')
    if request.method == "POST":
        post_data = request.POST
        if 'username' in post_data:
            try:
                user = User.objects.get(username=post_data['username'])
            except:
                response['result'] = 'error'
                response['msg'] = 'Пользователь не найден'
                return HttpResponse(json.dumps(response), content_type="application/json")
            if 'password' in post_data:
                user = authenticate(username=post_data['username'], password=post_data['password'])
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        response['result'] = 'ok'
                        response['msg'] = "Авторизация ок!"
                        return HttpResponse(json.dumps(response), content_type="application/json")
                    else:
                        response['result'] = 'error'
                        response['msg'] = "Пользователь не активен"
                        return HttpResponse(json.dumps(response), content_type="application/json")
                else:
                    response['result'] = 'error'
                    response['msg'] = 'Пароль введен неверно'
                    return HttpResponse(json.dumps(response), content_type="application/json")

        else:
            response['result'] = 'error'
            response['msg'] = 'Пароль не введен'
            return HttpResponse(json.dumps(response), content_type="application/json")

        #return HttpResponse(json.dumps({'answer': "POST"}), content_type="application/json")

@login_required
def signOff(request):
    logout(request)
    return redirect("/login/")

