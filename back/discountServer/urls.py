"""discountServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import RedirectView

from rest_framework.authtoken import views as auth

from discountServer import views
from transactions import views as t_views
from queues import views as q_views
from service import views as s_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.signIn, name='signIn'),
    url(r'^logout/$', views.signOff, name='signOff'),
    url(r'^settings/$', views.settings, name='settings'),
    url(r'^settings/discount/$', views.settings_discount, name='settings_discount'),
    url(r'^settings/workplace/$', views.settings_workplace, name='settings_workplace'),
    url(r'^settings/org/$', views.settings_org, name='settings_org'),
    url(r'^service/$', s_views.list_service, name='list_service'),
    url(r'^transactions/$', t_views.listTrans, name='listTrans'),
    url(r'^transactions/api/', include('transactions.rest_urls')),
    url(r'^queue/$', q_views.listQueue, name='listQueue'),
    url(r'^settings/save/$', views.settingsSave, name='settingsSave'),
    url(r'^settings/frontol/$', views.exportFrontolSettings, name='exportFrontolSettings'),
    url(r'^settings/api/', include('core.rest_urls')),
    url(r'^cards/', include('cards.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^favicon.ico$', RedirectView.as_view(url='/static/images/favicon.ico'), name='favicon'),


    url(r'^auth/$', auth.obtain_auth_token),

    url(r'^', views.index),

]
