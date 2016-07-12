"""Use newstyle callable imports for view names, rather than string imports, per Django 10 Deprecation."""

from django.conf.urls import url
from django.contrib import admin
from core import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'(?P<city>[^/]+)/(?P<period_in_days>[0-9]{1,2})/$', views.weather_endpoint),
    url(r'^admin/', admin.site.urls),
]

#(?P<period_in_days>[0-9]{2})
