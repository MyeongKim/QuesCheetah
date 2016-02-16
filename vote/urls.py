# 직접 개발한 코드
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from vote import views

urlpatterns = [

    # QuesCheetah Web Server URLS

    url(r'^select/(?P<api_key>\w+)$', views.select_question, name='select_question'),
    url(r'^get/multiple/(?P<api_key>\w+)/(?P<group_name>[\w|\W]+)$', views.get_multiple_vote, name='get_multiple_vote'),
    url(r'^get/(?P<api_key>\w+)/(?P<question_id>\d+)$', views.get_vote, name='get_vote'),
    url(r'^new/(?P<api_key>\w+)$', views.new, name='new'),
    url(r'^dashboard/(?P<api_key>\w+)/(?P<question_id>\w+)$', views.dashboard, name='dashboard'),
    url(r'^dashboard/multiple/(?P<api_key>\w+)/(?P<group_name>[\w|\W]+)$', views.multiple_dashboard, name='multiple_dashboard'),

    # REST API URLS

    # GET, PUT, DELETE
    url(r'^groups/(?P<group_id>\d+)', csrf_exempt(views.Groups.as_view()), name='group'),
    # POST
    url(r'^groups$', csrf_exempt(views.Groups.as_view()), name='group_post'),

    # GET
    url(r'^questions/(?P<question_id>\w+)/SimpleResult$', views.simple_view_answer, name='question_simple_result'),
    # GET
    url(r'^questions/(?P<question_id>\w+)/ToPrivate$', views.to_private, name='question_to_private'),
    # GET(full), PUT, DELETE
    url(r'^questions/(?P<question_id>\w+)$', csrf_exempt(views.Questions.as_view()), name='question'),
    # POST
    url(r'^questions$', csrf_exempt(views.Questions.as_view()), name='question_post'),

    # POST, GET, PUT
    url(r'^questions/(?P<question_id>\w+)/answers/$', csrf_exempt(views.Answers.as_view()), name='answer_post'),
    # GET, DELETE
    url(r'^questions/(?P<question_id>\w+)/answers/(?P<answer_num>\d+)$', csrf_exempt(views.Answers.as_view()), name='answer'),
    # GET
    url(r'^questions/(?P<question_id>\w+)/answers/useranswers/$', csrf_exempt(views.Useranswers.as_view()), name='useranswer'),
    # GET, DELETE, PUT
    url(r'^questions/(?P<question_id>\w+)/answers/useranswers/(?P<unique_user>\w+)$', csrf_exempt(views.Useranswers.as_view()), name='useranswer'),
    # POST, GET
    url(r'^questions/(?P<question_id>\w+)/answers/(?P<answer_num>\d+)/useranswers$', csrf_exempt(views.Useranswers.as_view()), name='useranswer_post'),
]
