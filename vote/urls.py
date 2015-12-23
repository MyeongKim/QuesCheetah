from django.conf.urls import url
from vote import views

urlpatterns = [
    url(r'^select/(?P<api_key>\w+)$', views.select_question, name='select_question'),
    url(r'^get/(?P<api_key>\w+)/(?P<question_title>\w+)$', views.get_vote, name='get_vote'),
    # url(r'^action/(?P<api_key>\w+)$', views.action, name='action'),
    url(r'^new/(?P<api_key>\w+)$', views.new, name='new'),
    url(r'^useranswer/create', views.create_useranswer, name='create_useranswer'),
    url(r'^answer/simple_view', views.simple_view_answer, name='simple_view_answer'),
    url(r'^dashboard/(?P<api_key>\w+)/(?P<question_id>\w+)$', views.dashboard, name='dashboard'),

]