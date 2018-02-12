from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render


# Create your views here.
@login_required
def get_user(request):
    response = {'first_name': request.user.first_name,
                'last_name': request.user.last_name}
    return JsonResponse(response)
