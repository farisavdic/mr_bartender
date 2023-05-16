from .models import Cup, ApiKey
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
def get_order(cup_id):
    c = Cup.objects.get(cup_id=cup_id)
    order = c.order
    c.order = ""
    c.save()
    return order
