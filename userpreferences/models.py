from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

from bonds.models import Bond
from shares.models import Share


class UserPreference(models.Model):
    name = models.CharField(max_length=50)
    creation_date = models.DateField(default=now)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    shares = models.ManyToManyField(Share)
    bonds = models.ManyToManyField(Bond)

    objects = models.Manager()

    def __str__(self):
        return str(self.user)+'s' + 'preferences'

    class Meta:
        ordering: ['creation_date', 'name']
