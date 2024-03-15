from django.contrib import admin
from django.urls import path
from intro import views

app_name="intro"
urlpatterns = [
    path("", views.index),
    path("detail/<str:local>",views.detail, name="detail")
]
