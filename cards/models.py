from django.db import models
from orgs import models as org_models
# Create your models here.

class Card (models.Model):
    code = models.CharField(max_length=20)
    accumulation = models.FloatField(default='0')
    org = models.ForeignKey(org_models.Org, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("code", "org"),)

