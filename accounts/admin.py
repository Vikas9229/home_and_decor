from django.contrib import admin

from .models import Account,UserProfile,Designer
# Register your models here.
admin.site.register(Account)
admin.site.register(UserProfile)
admin.site.register(Designer)