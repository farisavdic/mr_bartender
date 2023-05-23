import csv
from cocktails.models import *

with open("cocktails2.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=';')
    #tmp = next(csv_reader)
    tmp = next(csv_reader)
    for t in tmp:
        ing = IngredientForDrink(name=t)
        ing.save()
        #print(t)

