# 직접 개발한 코드
from django.conf.urls import url
from main import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.user_login, name='user_login'),
    url(r'^logout', views.user_logout, name='user_logout'),
    url(r'^signup$', views.user_signup, name='user_signup'),
    url(r'^user/(?P<id>\w+)', views.user_mypage, name='user_mypage'),
    url(r'^apikey/new', views.apikey_new, name='apikey_new'),
    url(r'^domain/new', views.domain_new, name='domain_new'),
]