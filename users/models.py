from django.db import models
from django.contrib.auth.models import User
from orgs import models as org_models


class UserCustom(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    org = models.ForeignKey(org_models.Org, on_delete=models.CASCADE)
