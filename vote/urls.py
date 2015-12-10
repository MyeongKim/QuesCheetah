from django.conf.urls import url
from vote import views

urlpatterns = [
    url(r'^new/(?P<api_key>\w+)$', views.new, name='new'),
]