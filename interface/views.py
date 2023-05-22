from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from cocktails.models import Drink
from api.utils import get_available_drinks


# Create your views here.
def index(request):
    available_drinks = get_available_drinks()
    template = loader.get_template("interface/index.html")
    context = {
        "available_drinks": available_drinks,
        "api_key": request.GET.get("api_key", default=""),
        "cup_id": request.GET.get("cup_id", default=""),
    }
    return HttpResponse(template.render(context, request))


def order(request):
    drink_name = request.GET.get("drink", default="")
    #drink_name = drink_name[:-1]
    d = Drink.objects.filter(name=drink_name)
    template = loader.get_template("interface/order.html")
    if d:
        context = {
            "drink_name": drink_name,
            "ingredients": d[0].ingredients.all(),
            "api_key": request.GET.get("api_key", default=""),
            "cup_id": request.GET.get("cup_id", default=""),
        }
    else:
        context = {
            "drink_name": None,
        }
    return HttpResponse(template.render(context, request))
