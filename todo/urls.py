from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path("", views.home,name="home"),
    path("login/", views.login,name="login"),
    path("registration/", views.registration,name="registration"),
    path("todo_list", views.todo_list,name="todo_list"),#destination
    path("add", views.add,name="add"),
    path("todo_detail", views.todo_detail,name="todo_detail"),
    path("delete/<int:id>", views.delete,name="delete"),
    path("logout/", views.logout,name="logout"),
    path("finished/<int:id>", views.finished,name="finished"),
    path("display/<int:id>", views.display,name="display"),
    path('admindash', views.admindash, name='admindash'),
    # path("perform_update", views.perform_update, name="performUpdate"),
    # path("perform_delete", views.perform_delete, name="perform_delete"),
]
