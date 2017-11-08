from django.conf.urls import url, include
from cards import views

urlpatterns = [
    url(r'cards/(?P<org_id>[0-9]+)_(?P<card_code>[0-9]+)_(?P<salt>0.[0-9]+)/$', views.apiGetCard, name='apiGetCard'),
    url(r'cards/add_accum/(?P<org_id>[0-9]+)_(?P<card_code>[0-9]+)_(?P<salt>0.[0-9]+)/$',
        views.apiAddAccumToCard, name='apiAddAccumToCard'),


]
