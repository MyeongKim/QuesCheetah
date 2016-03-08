# 직접 개발한 코드
from django.conf.urls import url
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import condition
from vote import views
import datetime

urlpatterns = [

    # QuesCheetah Web Server URLS

    url(r'^select$', views.select_question, name='select_question'),
    url(r'^get/multiple/(?P<api_key>\w+)/(?P<group_name>[\w|\W]+)$', views.get_multiple_vote, name='get_multiple_vote'),
    url(r'^get/(?P<api_key>\w+)/(?P<question_id>\d+)$', views.get_vote, name='get_vote'),
    url(r'^new/(?P<api_key>\w+)$', views.new, name='new'),

    # Dashboard management url

    url(r'dashboard/select$', views.dashboard_select, name='dashboard_select'),
    url(r'dashboard/groups/(?P<group_id>\w+)/overview$', views.dashboard_group_overview, name='dashboard_group_overview'),
    url(r'dashboard/(?P<question_id>\w+)/overview$', views.dashboard_overview, name='dashboard_overview'),
    url(r'dashboard/groups/(?P<group_id>\w+)/filter$', views.dashboard_group_filter, name='dashboard_group_filter'),
    url(r'dashboard/(?P<question_id>\w+)/filter$', views.dashboard_filter, name='dashboard_filter'),
    url(r'dashboard/groups/(?P<group_id>\w+)/users$', views.dashboard_group_users, name='dashboard_group_users'),
    url(r'dashboard/(?P<question_id>\w+)/users$', views.dashboard_users, name='dashboard_users'),

    # REST API URLS

    # GET
    url(r'^groups/(?P<group_id>\w+)/answers/useranswers$', csrf_exempt(views.Useranswers.as_view())),
    # GET, PUT, DELETE
    url(r'^groups/(?P<group_id>\d+)$', csrf_exempt(views.Groups.as_view()), name='group'),
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
