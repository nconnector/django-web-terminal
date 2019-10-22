from django.contrib import admin

# Register your models here.
from .models import Case, Account

admin.site.register(Account)
admin.site.register(Case)
