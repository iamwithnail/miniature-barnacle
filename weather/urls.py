"""Use newstyle callable imports for view names, rather than string imports, per Django 10 Deprecation."""

from django.conf.urls import url
from django.contrib import admin
from core import views

urlpatterns = [
    url(r'(?P<city>[^/]+)/(?P<period_in_days>[0-9]{1,2})/$', views.weather_endpoint),
    url(r'(?P<city>[^/]+)/(?P<period_in_days>[0-9]{1,2})/graph/$', views.graph_endpoint),
    url(r'^$', views.root),
    url(r'^admin/', admin.site.urls),
]

handler404 = views.page_not_found
