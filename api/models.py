from django.db import models
from cocktails.models import Ingredient


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


class Dispenser(models.Model):
    dispenser_id = models.IntegerField(default=-1)
    ingredient = models.OneToOneField(Ingredient, on_delete=models.SET_NULL, null=True, unique=False)

    def __str__(self):
        if self.ingredient.available:
            availability = "available"
        else:
            availability = "unavailable"
        return "Dispenser" + str(self.dispenser_id) + ": " + self.ingredient.name + " (" + availability + ")"
