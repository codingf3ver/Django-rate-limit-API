from django.contrib import admin
from django.urls import path, include
from zmq import Message
from . import views


urlpatterns = [
   
    path('',views.home,name='home'),
    path('api/messages/',views.MessageView.as_view()),
]