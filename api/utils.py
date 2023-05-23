from .models import ApiKey, Cup, Dispenser
from cocktails.models import Ingredient, Drink
from decimal import Decimal
import secrets

# utility functions to be imported into other files


# generates 16 Byte API-key and saves it to database
def gen_api_key():
    key = secrets.token_urlsafe(16)
    k = ApiKey(key=key)
    k.save()
    return key


# returns True if <key> is master key
def is_master_key(key):
    if key == "2wY3Oc37F3MGLxqPnEGdwA":
        return True
    return False


# returns True if <key> is a valid API-key
def check_api_key(key):
    if ApiKey.objects.filter(key=key).exists():
        return True
    return False


# returns True if <cup_id> is actually associated with a registered cup
def check_cup_id(cup_id):
    c = Cup.objects.filter(cup_id=cup_id)
    if c:
        return True
    return False


# registers a cup with <cup_id> and boolean value <mixable>
def register_cup(cup_id, mixable):
    if check_cup_id(cup_id):
        return 2
    c = Cup(cup_id=cup_id, order="", mixable=mixable)
    c.save()
    return 1


# removes cup with <cup_id> from database
def delete_cup(cup_id):
    if check_cup_id(cup_id):
        c = Cup.objects.get(cup_id=cup_id)
        c.delete()
        return 1
    return 2


# adds <order> String to Cup-object in database with <cup_id>
def place_order(cup_id, order):
    c = Cup.objects.get(cup_id=cup_id)
    c.order = order
    c.save()
    return 1


# returns order-String associated with <cup_id>
def get_order(cup_id, encoded=False):
    c = Cup.objects.get(cup_id=cup_id)
    order = c.order
    c.order = ""
    c.save()
    if encoded:
        return arduino_encode(order)
    return order

# Gin:4.0;Tonic Water:12.0;Limette:1.0;0000
def arduino_encode(order):
    str_list = [None] * 12
    comp_list = order.split(";")

    str_list[0] = '0' # do not mix
    disps = Dispenser.objects.all()
    for e in comp_list:
        pair = e.split(":")
        #print(pair[0] + " " + pair[1])
        for d in disps:
            #print(d.dispenser_id)
            #print(d.ingredient)
            if d.ingredient.name == pair[0]:
                str_list[int(d.dispenser_id)+1] = str((Decimal(pair[1]) * 10))
    for i in range(12):
        if not str_list[i]:
            str_list[i] = ""
    return ":".join(str_list)




def get_available_drinks():
    av_drinks = list()
    av_ingredients = list()
    dispensers = Dispenser.objects.all()
    for d in dispensers:
        if d.ingredient.available:
            av_ingredients.append(d.ingredient.name)
        continue
    drinks = Drink.objects.all()
    for dr in drinks:
        available = True
        ingredients = dr.ingredients.all()
        for i in ingredients:
            if not i.name in av_ingredients:
                available = False
                break
            continue
        if available:
            av_drinks.append(dr.name)
    return av_drinks
