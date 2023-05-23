from django.urls import path

import interface.views
from . import views
from interface import views

urlpatterns = [
    path("", views.index, name="index"),
    path("index/", views.index, name="index"),
    path("order/", views.order, name="order"),
    path("message/", views.message, name="message"),
    path("message/interface/", interface.views.index, name="home"),
]
