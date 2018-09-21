"""anehome URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from . import settings
from .. import views
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from anehome_test.anehome.views import *

from anehome_test.anehome.startup_routine import startup_routine

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main),
    path('exp/', experiment),
    path('snaps/', list_snaps),
    path('cp/', display_cp),
    url('snaps/snap_(?P<year>[\d]+)_(?P<month>[\d]+)_(?P<day>[\d]+)__' +\
         '(?P<hour>[\d]+)_(?P<minute>[\d]+)_(?P<second>[\d]+)/', display_snap, {}),
    url(r'^display-price-table/', display_price_table, name='display-price-table'),
    url('dynamics/', dynamics, {}),


]

# urlpatterns += staticfiles_urlpatterns()
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

startup_routine()