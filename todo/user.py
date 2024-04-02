from .models import Person,User
from django.db import models

from django.db import models


def userlogin(request):
    if request.method == 'POST.get':
        email = request.POST.get('email')
        password = request.POST.get('password')
        Enc_password = (password)
        try:
            user = User.objects.get(username="admin")
            return
        except:
            pass