from django.conf.urls import url, include
from cards import views

urlpatterns = [

    url(r'^(?P<card_code>[0-9]+)/$', views.rest_card_by_code, name='rest_card_by_code'),
    url(r'^', views.rest_cards_list, name='rest_cards_list'),

]