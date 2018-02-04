from django.conf.urls import url
from transactions import views

urlpatterns = [

    url(r'^(?P<card_code>[0-9]+)/$', views.rest_trans_by_card, name='rest_trans_by_card'),
    url(r'^(?P<card_code>[0-9]+)/discount/$', views.rest_discount_trans_by_card, name='rest_discount_trans_by_card'),
    url(r'^', views.rest_transactions_list, name='rest_transactions_list'),

]
