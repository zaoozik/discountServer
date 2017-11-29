from django.conf.urls import url, include
from api import views

urlpatterns = [
    url(r'^cards/(?P<card_code>[0-9]+)_(?P<salt>0.[0-9]+)/$', views.apiGetCard, name='apiGetCard'),
    url(r'^cards/add_accum/(?P<card_code>[0-9]+)_(?P<salt>0.[0-9]+)/$',
        views.apiAddAccumToCard, name='apiAddAccumToCard'),
    url(r'^cards/rem_bonus/(?P<card_code>[0-9]+)_(?P<salt>0.[0-9]+)/$',
        views.apiRemCardBonus, name='apiRemCardBonus'),
    url(r'^cards/vti_keeper/$',
        views.apiToCardFromService, name='apiToCardFromService'),
    url(r'^get_params/(?P<salt>0.[0-9]+)/$', views.apiGetParams, name='apiGetParams'),


]
