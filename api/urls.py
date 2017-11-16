from django.conf.urls import url, include
from api import views

urlpatterns = [
    url(r'^cards/bonus/(?P<org_id>[0-9]+)_(?P<card_code>[0-9]+)_(?P<salt>0.[0-9]+)/$', views.apiGetCardBonus, name='apiGetCardBonus'),
    url(r'^cards/discount/(?P<org_id>[0-9]+)_(?P<card_code>[0-9]+)_(?P<salt>0.[0-9]+)/$', views.apiGetCardDiscount, name='apiGetCardDiscount'),
    url(r'^cards/add_accum/(?P<org_id>[0-9]+)_(?P<card_code>[0-9]+)_(?P<salt>0.[0-9]+)/$',
        views.apiAddAccumToCard, name='apiAddAccumToCard'),
    url(r'^cards/rem_bonus/(?P<org_id>[0-9]+)_(?P<card_code>[0-9]+)_(?P<salt>0.[0-9]+)/$',
        views.apiRemCardBonus, name='apiRemCardBonus'),
    url(r'^get_plan/(?P<salt>0.[0-9]+)/$', views.apiGetDiscountPlan, name='apiGetDiscountPlan'),


]
