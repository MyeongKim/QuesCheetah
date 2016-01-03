from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_view


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^password/reset/done/$', auth_view.password_reset_done, name='password_reset_done'),
    url(r'^password/reset/$', auth_view.password_reset, name='password_reset'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)', auth_view.password_reset_confirm, name='password_reset_confirm'),
    url(r'^password/reset/confirm/complete/$', auth_view.password_reset_complete, name='password_reset_complete'),

    url(r'^accounts/', include('allauth.urls')),

    url(r'vote/', include('vote.urls', namespace='vote')),
    url(r'', include('main.urls', namespace='main')),


]
