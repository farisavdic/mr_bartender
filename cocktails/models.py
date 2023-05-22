from django.db import models


# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=40)
    amount = models.DecimalField(decimal_places=1, max_digits=3, default=1.0)
    unit = models.CharField(max_length=5, default="cl")
    alcoholic = models.BooleanField(default=False)
    garnish = models.BooleanField(default=False)
    available = models.BooleanField(default=False)

    def __str__(self):
        return self.name + ": " + str(self.amount) + " " + self.unit


class Drink(models.Model):
    name = models.CharField(max_length=40)
    ingredients = models.ManyToManyField(Ingredient)
    alcoholic = models.BooleanField(default=True)

    def print_ingredients(self):
        ings = self.ingredients.all()
        string = ""
        for i in ings:
            string = string + str(i) + "\n"
        return string

    def __str__(self):
        return self.name + ":\n" + self.print_ingredients()


