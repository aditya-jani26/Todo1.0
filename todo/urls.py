from django.urls import path
from .views import *
from todo import views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('todo/', TodoView.as_view(), name='todo'),

    path('finished/<int:id>/', FinishedView.as_view(), name='finished'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('delete/<int:id>/', DeleteView.as_view(), name='delete'),
    path('display/<int:id>/', DisplayView.as_view(), name='display'),
    path('admindash/', AdminDashView.as_view(), name='admindash'),
]
