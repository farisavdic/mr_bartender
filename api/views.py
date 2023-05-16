from django.shortcuts import render, redirect
from django.http import HttpResponse
from .utils import *


# Create your views here.
def index(request):
    api_key = request.GET.get("key", "")
    if not check_api_key(api_key):
        return HttpResponse("Please use valid API key")
    action = request.GET.get("action", "-1")
    if action == "-1":
        return HttpResponse("Please use action code")
    if action == '1':
        cup_id = request.GET.get("cup_id", "")
        if check_cup_id(cup_id):
            mixable = request.GET.get("mixable", False)
            code = register_cup(cup_id, mixable)
            if code == 2:
                return HttpResponse("Cup is already registered")
            elif code == 1:
                return HttpResponse("Successfully registered cup with id " + str(cup_id) + " .")
            else:
                return HttpResponse("Error while saving to database")
        else:
            return HttpResponse("invalid cup_id")

    elif action == '2':
        cup_id = request.GET.get("cup_id", "")
        if check_cup_id(cup_id):
            code = delete_cup(cup_id)
            if code == 1:
                return HttpResponse("Successfully deleted cup with id " + str(cup_id) + " .")
            elif code == 2:
                return HttpResponse("Cup with id " + str(cup_id) + " does not exist")
            else:
                return HttpResponse("Error while deleting from database")
        else:
            return HttpResponse("invalid cup_id")

    elif action == '3':
        cup_id = request.GET.get("cup_id", "")
        if check_cup_id(cup_id):
            order = request.GET.get("order", "")
            if order:
                if place_order(cup_id, order):
                    return HttpResponse("Successfully placed order for cup " + str(cup_id))
                return HttpResponse("Error while placing order")
            else:
                return HttpResponse("missing order")
        else:
            return HttpResponse("invalid cup_id")

    elif action == '4':
        cup_id = request.GET.get("cup_id", "")
        if check_cup_id(cup_id):
            order = get_order(cup_id)
            if order:
                return HttpResponse(order + " was successfully prepared")
            return HttpResponse("There is no order for cup " + str(cup_id))
        else:
            return HttpResponse("invalid cup_id")

    elif action == '5':
        if is_master_key(api_key):
            key = gen_api_key()
            return HttpResponse("API key is " + key)
        return HttpResponse("You are not authorized to generate API keys")

    else:
        return HttpResponse("invalid action code")
