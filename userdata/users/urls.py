from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^list/', views.listUsers, name='list'),
    url(r'^add/', views.add, name='add')
]
