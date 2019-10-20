from django.contrib import admin

# Register your models here.
from .models import Case, Client

admin.site.register(Case)
admin.site.register(Client)
