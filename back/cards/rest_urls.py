from django.conf.urls import url, include
from cards import views

urlpatterns = [

    url(r'^(?P<card_code>[0-9]+)/$', views.rest_card_by_code, name='rest_card_by_code'),
    url(r'^(?P<card_code>[0-9]+)/add_bonus/$', views.rest_add_bonus, name='rest_add_bonus'),
    url(r'^new/$', views.rest_new_card, name='rest_new_card'),
    url(r'^', views.rest_cards_list, name='rest_cards_list'),

]
