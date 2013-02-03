from django.conf.urls import patterns, url
from correlations import views


urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<correlation_id>\d+)/$', views.detail, name='detail'),
    url(r'^(?P<correlation_id>\d+)/simple_plot/$', views.simple_plot,
        name='simple_plot'),
)
