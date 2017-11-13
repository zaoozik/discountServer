from django.db import models
from orgs import models as org_models
# Create your models here.

class Card (models.Model):
    code = models.CharField(max_length=20)
    accumulation = models.FloatField(default=0)
    bonus = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    holder_name = models.CharField(max_length=100, default='')
    org = models.ForeignKey(org_models.Org, on_delete=models.CASCADE)
    deleted = models.CharField(max_length=1, default='n')

    def __str__(self):
        return self.org.name + "_" + self.code

    class Meta:
        unique_together = (("code", "org"),)

