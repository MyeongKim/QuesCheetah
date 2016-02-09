# 직접 개발한 코드
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from vote import views

urlpatterns = [
    url(r'^select/(?P<api_key>\w+)$', views.select_question, name='select_question'),
    url(r'^get/multiple/(?P<api_key>\w+)/(?P<group_name>[\w|\W]+)$', views.get_multiple_vote, name='get_multiple_vote'),
    url(r'^get/(?P<api_key>\w+)/(?P<question_title>[\w|\W]+)$', views.get_vote, name='get_vote'),
    url(r'^new/(?P<api_key>\w+)$', views.new, name='new'),
    url(r'^dashboard/(?P<api_key>\w+)/(?P<question_id>\w+)$', views.dashboard, name='dashboard'),
    url(r'^dashboard/multiple/(?P<api_key>\w+)/(?P<group_name>[\w|\W]+)$', views.multiple_dashboard, name='multiple_dashboard'),


    url(r'^multiple/create', views.create_multiple_question, name='create_multiple_question'),
    url(r'^multiple/get', views.get_group, name='get_multiple_question'),
    url(r'^multiple/delete', views.delete_multi_question_set, name='delete_multi_question_set'),

    url(r'^single/create', views.create_single_question, name='create_single_question'),

    url(r'^question/create', views.create_question, name='create_question'),
    url(r'^question/get', views.get_question, name='get_question'),
    url(r'^question/delete', views.delete_question, name='delete_question'),
    url(r'^question/set/delete', views.delete_question_set, name='delete_question_set'),
    url(r'^question/private', views.to_private, name='to_private'),

    url(r'^answer/create', views.create_answer, name='create_answer'),
    url(r'^answer/view/simple', views.simple_view_answer, name='simple_view_answer'),
    url(r'^answer/get', views.get_answer, name='get_answer'),
    url(r'^answer/delete', views.delete_answer, name='delete_answer'),

    url(r'^useranswer/create', views.create_useranswer, name='create_useranswer'),
    url(r'^useranswer/delete', views.delete_useranswer, name='delete_useranswer'),
    url(r'^useranswer/update', views.update_useranswer, name='update_useranswer'),


    # updated REST API URLs


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
    # GET, DELETE,
    url(r'^questions/(?P<question_id>\w+)/answers/(?P<answer_num>\d+)$', csrf_exempt(views.Answers.as_view()), name='answer'),

    url(r'^questions/(?P<question_id>\w+)/answers/useranswers/$', csrf_exempt(views.Useranswers.as_view()), name='useranswer'),
    # GET, DELETE, PUT
    url(r'^questions/(?P<question_id>\w+)/answers/useranswers/(?P<unique_user>\w+)$', csrf_exempt(views.Useranswers.as_view()), name='useranswer'),
    # POST, GET
    url(r'^questions/(?P<question_id>\w+)/answers/(?P<answer_num>\d+)/useranswers$', csrf_exempt(views.Useranswers.as_view()), name='useranswer_post'),
]
