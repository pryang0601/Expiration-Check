from django.contrib import admin

# Register your models here.
from foodlinebot.models import *

class Food_Info_Admin(admin.ModelAdmin):
    list_display = ('name','start','expiration')
    search_fields=('name',)
    ordering=('expiration',)
admin.site.register(Food_Info,Food_Info_Admin)
