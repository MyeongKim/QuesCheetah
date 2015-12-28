from django.conf.urls import url
from vote import views

urlpatterns = [
    url(r'^select/(?P<api_key>\w+)$', views.select_question, name='select_question'),
    url(r'^get/(?P<api_key>\w+)/(?P<question_title>\w+)$', views.get_vote, name='get_vote'),
    url(r'^get/multiple/(?P<api_key>\w+)/(?P<group_name>\w+)$', views.get_multiple_vote, name='get_multiple_vote'),
    # url(r'^action/(?P<api_key>\w+)$', views.action, name='action'),
    url(r'^new/multiple/(?P<api_key>\w+)$', views.new_multiple, name='new_multiple'),
    url(r'^new/(?P<api_key>\w+)$', views.new, name='new'),
    url(r'^useranswer/create', views.create_useranswer, name='create_useranswer'),
    url(r'^multiple/create', views.create_multiple_question, name='create_multiple_question'),
    url(r'^single/create', views.create_single_question, name='create_single_question'),
    url(r'^answer/view/simple', views.simple_view_answer, name='simple_view_answer'),
    url(r'^dashboard/(?P<api_key>\w+)/(?P<question_id>\w+)$', views.dashboard, name='dashboard'),
    url(r'^dashboard/multiple/(?P<api_key>\w+)/(?P<group_name>\w+)$', views.multiple_dashboard, name='multiple_dashboard'),

]