from django.conf.urls import url
from CapApp import views

#Get a someone to help you with this.
urlpatterns = [

    url(r'^$', views.grants, name='grants'),
    url(r'^publications', views.publications, name='publications'),
]
