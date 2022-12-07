from django.contrib import admin
from .models import *
# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    list_display =  ['first_name','last_name','phone' ]


admin.site.register(CustomUser)
