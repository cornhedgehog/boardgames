from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^countries/$', views.countries, name='countries'),
    url(r'^cities_by_country/(?P<country_id>\d+)/$', views.cities_by_country, name='cities_by_country'),
]
