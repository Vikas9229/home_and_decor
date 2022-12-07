from datetime import date
from email.policy import default
import json
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
# type of users we have in the system will be saved in to the database and we can assign different roles to them


# custoUser is inherited by the AbstractUser class and adding extra field to it.
class CustomUser(AbstractUser):
    phone = models.CharField(max_length=14,null=True,blank=True)
    image = models.ImageField(null=True,blank=True)

    def get_full_name(self):
        return str(self.first_name + " " + self.last_name)
        


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
