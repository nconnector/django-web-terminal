from django.contrib import admin

# Register your models here.
from .models import Case, Account, Script, Advert

admin.site.register(Account)
admin.site.register(Case)
admin.site.register(Script)
admin.site.register(Advert)
