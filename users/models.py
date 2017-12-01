from django.db import models
from django.contrib.auth.models import User
from orgs import models as org_models
import random
import uuid
from datetime import datetime


class UserCustom(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    org = models.ForeignKey(org_models.Org, on_delete=models.CASCADE)
    frontol_access_key = models.CharField(max_length=64, null=True)
    active_to = models.DateField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=['frontol_access_key'], name='frontol_access_key_index'),
        ]

    def cu_is_active(self):
        if self.active_to >= datetime.now():
            return True
        else:
            return False

    def init_frontol_access_key(self):
        if self.frontol_access_key is None:
            self.frontol_access_key = '%030x' % random.randrange(16**64)

