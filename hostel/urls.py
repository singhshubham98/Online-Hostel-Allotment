from django.conf.urls import url
from . import views

app_name = 'hostel'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.logout1, name='logout'),
    # url(r'^allocate/$', views.allocate, name='allocate'),
]