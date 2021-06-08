from django.conf.urls import url
from . import views
urlpatterns = [url('^$', views.poll_index, name='poll'), url(
    '^statistics/$', views.statistics, name='statistics'), url(
    '^statistics/get_data/$', views.get_data, name='get_data')]
