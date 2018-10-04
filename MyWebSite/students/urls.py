from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^thanks/$', views.thankyou, name='thankyou'),
    url(r'students/signup/$', views.signup, name='signup'),
    url(r'students/signin/$', views.signin, name='signin'),
    url(r'students/logout/$', views.logoutView, name='logout'),
    url(r'students/(?P<visualizationId>\w+)', views.showVisualizations, name='students'),
    url(r'students/create/$', views.createStudent, name='createStudent'),
    url(r'subjects/$', views.getSubjects, name='subjects'),
    url(r'students/search/$', views.search, name='search'),
    url(r'students/rank/$', views.rank, name='rank'),
    url(r'logout/$', views.logoutView, name='logout'),
    # url(r'^students/pagination$', views.StudentsList.as_view(), name='paginatedStudents'),
    # url(r'^students/pagination/ajax/$', views.ajaxView, name='ajaxScrollUpStudents'),
    # url(r'^students/pagination/ajax/_scroll/$', views.paginateStudentsByAjax),
]