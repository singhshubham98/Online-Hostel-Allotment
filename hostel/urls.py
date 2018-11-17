
from django.conf.urls import url
from . import views

app_name = 'hostel'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.logout1, name='logout'),
    url(r'^allocate/$', views.allocate, name='allocate'),
    url(r'^student_details/$', views.student_details, name='student_details'),
    url(r'^change/$', views.change, name='change'),
    url(r'^change_req/$', views.change_request, name='change_req'),
    url(r'^swap/$', views.swap, name='swap'),
    url(r'^swap_req/$', views.swap_request, name='swap_request'),
    url(r'^success/$', views.success, name='success'),
    url(r'^swap_ack/$', views.swap_ack, name='swap_ack'),
    url(r'^deallocate/$', views.deallocate, name='deallocate'),
    url(r'^show_request/$', views.show_request, name='show_request'),
    url(r'^show_vacancy/$', views.vacant_room, name='show_vacancy'),
    url(r'^show_students/$', views.show_students, name='show_students'),
]
