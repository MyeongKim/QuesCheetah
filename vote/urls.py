from django.conf.urls import url
from vote import views

urlpatterns = [
    url(r'^action/(?P<api_key>\w+)$', views.action, name='action'),
    url(r'^new/(?P<api_key>\w+)$', views.new, name='new'),
    url(r'^update', views.update, name='update'),
]