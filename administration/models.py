# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from django.db import models

# Create your models here.
# class Profile(models.Model):
#     user = models.OneToOneField(User, related_name="user_id")

#     profile_types = {
#         "user": 1,
#         "superuser": 2,
#         "admin": 3,
#     }

#     TYPE_CHOICES = []
#     id_types = {}
#     for name, index in profile_types.items():
#         TYPE_CHOICES.append((index, name))
#         id_types[index] = name
#     profile_type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)

#     def __unicode__(self):
#         return self.user.username

#     class Meta:
#         permissions = (
#             ("user", u"user permission"),
#             ("superuser", u"superuser permission"),
#             ("admin", u"admin permission"),
#         )

#         db_table = 'profile'

class Users(models.Model):
    ip = models.CharField(max_length=10)
    datetime = models.DateTimeField()
