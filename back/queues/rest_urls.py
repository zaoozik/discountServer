from django.conf.urls import url
from queues import views

urlpatterns = [


    url(r'^api/', views.rest_task_list, name='rest_task_list'),

]
