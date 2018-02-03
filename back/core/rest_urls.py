from django.conf.urls import url
from core import views

urlpatterns = [

    url(r'^$', views.rest_get_discount_plan, name='rest_get_discount_plan'),
    # url(r'^(?P<card_code>[0-9]+)/discount/$', views.rest_discount_trans_by_card, name='rest_discount_trans_by_card'),

    #url(r'^', views.rest_cards_list, name='rest_cards_list'),

]
