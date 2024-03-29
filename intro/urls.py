from django.contrib import admin
from django.urls import path
from intro import views

app_name="intro"
urlpatterns = [
    path("", views.index),
    path("detail/<str:local>",views.detail, name="detail"),
    path("check/",views.check, name="check"),
    path("tag/<str:tagName>",views.tag, name="tag"),
]
