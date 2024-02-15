from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path("", views.home,name="home"),
    path("login/", views.login,name="login"),
    path("registration/", views.registration,name="registration"),
    path("todo", views.todo,name="todo"),#destination
    path("add", views.add,name="add"),
    path("delete/<int:id>", views.delete,name="delete"),
    path("logoutuser", views.logoutuser,name="logoutuser"),
    path("completed/<int:id>", views.completed,name="completed"),
    path("display/<int:id>", views.display,name="display"),
    path('adminDash', views.adminDash, name='adminDash'),
]
