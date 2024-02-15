from django.contrib import admin
from.models import *

class PersonModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email"]
admin.site.register(Person)
admin.site.register(Todo)
