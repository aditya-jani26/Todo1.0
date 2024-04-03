from django.urls import path
from .views import *


urlpatterns = [
    path('registration/', RegistrationView.as_view(), name='registration'),
    # path('', HomeView.as_view(), name='home'),
    path('login/', LoginView.as_view(), name='login'),
    path('todo/', TodoView.as_view(), name='todo'),
    # path('admindash/', admindash_view.as_view(), name='admindash'),
]
