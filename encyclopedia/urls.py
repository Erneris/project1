from django.urls import path, include
from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', views.index, name = ""),
    path("wiki/<str:name>", views.page, name=""),
    path("wiki", views.wiki, name=""),
    path("edit", views.editroot, name=""),
    path("search", views.search, name="search"),
    path("create", views.create, name="create"),
    path("edit/<str:name>", views.edit, name=""),
    path("random", views.random, name="")
]