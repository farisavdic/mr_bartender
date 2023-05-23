from django.db import models


# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=40)
    available = models.BooleanField(default=False)
    unit = models.CharField(max_length=5, default="cl")
    garnish = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class IngredientForDrink(models.Model):
    name = models.CharField(max_length=40)
    amount = models.DecimalField(decimal_places=1, max_digits=3, default=1.0)
    mother_instance = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        return self.name + ": " + str(self.amount) + " " + self.mother_instance.unit


class Drink(models.Model):
    name = models.CharField(max_length=40)
    ingredients = models.ManyToManyField(IngredientForDrink)
    def __str__(self):
        return self.name


