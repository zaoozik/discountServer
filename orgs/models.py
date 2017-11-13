from django.db import models

# Create your models here.
class Org (models.Model):
    name = models.CharField(max_length=200)
    active_from = models.DateTimeField(null=True)
    active_to = models.DateTimeField(null=True)
    discount_plan = models.CharField(max_length=3, default='')

    def __str__(self):
        return self.name
