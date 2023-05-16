from django.db import models


# Create your models here.
class Cup(models.Model):
    cup_id = models.IntegerField(default=-1)
    order = models.CharField(max_length=1000, blank=True, null=True)
    mixable = models.BooleanField(default=False)

    def __str__(self):
        return "Cup " + str(self.cup_id)


class ApiKey(models.Model):
    key = models.CharField(max_length=22)

    def __str__(self):
        return self.key
