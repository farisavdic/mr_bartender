from .models import ApiKey, Cup, Dispenser
from cocktails.models import Ingredient, Drink
from decimal import Decimal
import secrets
from django.db.models.signals import post_save
from django.dispatch import receiver
import qrcode
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
def get_order(cup_id, encoded=False, prepare_drink=False):
    c = Cup.objects.get(cup_id=cup_id)
    order = c.order
    c.order = ""
    c.save()
    if prepare_drink:
        pass
        edit_amounts(order)
    if encoded:
        return arduino_encode(order)
    return order


def edit_amounts(order):
    print("order: "+ order)
    comp_list = order.split(";")
    dict = {}
    for c in comp_list:
        if c:
            pair = c.split(":")
            print(pair)
            dict[pair[0]] = pair[1]
    for ing in dict:
        d = Dispenser.objects.get(ingredient=Ingredient.objects.get(name=ing))
        d.amount_left = d.amount_left - Decimal(dict[ing])
        d.save()


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
                str_list[int(d.dispenser_id)+1] = str(int(Decimal(pair[1]) * 10))
    for i in range(12):
        if not str_list[i]:
            str_list[i] = ""
    str_list[11] = "0000"
    return ":".join(str_list)


def raise_warning(warning):
    pass


@receiver(post_save, sender=Dispenser)
def update(sender, instance, **kwargs):
    if instance.get_amount_left() > 10.0:
        instance.ingredient.available = True
        instance.ingredient.save()
    else:
        instance.ingredient.available = False
        instance.ingredient.save()
        raise_warning(str(instance.dispenser_id) + " is running low")


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

def gen_qr_code(data):
    qr = qrcode.QRCode(version=1,box_size=10,border=5)
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.save('qrcode001.png')
    return "qrcode001.png"
