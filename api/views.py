from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse
from .utils import *


# Create your views here.
def index(request):
    api_key = request.GET.get("key", "")
    if not check_api_key(api_key):
        return redirect("/interface/message/?api_key="+str(api_key)+"&cup_id="+str(cup_id)+"&message[]=Please%20use%20valid%20API%20key")
    action = request.GET.get("action", "-1")
    if action == "-1":
        return redirect("/interface/message/?api_key="+str(api_key)+"&cup_id="+str(cup_id)+"&message[]=Please%20use%20action%20code")
    if action == '1':
        cup_id = request.GET.get("cup_id", "")
        mixable = request.GET.get("mixable", False)
        code = register_cup(cup_id, mixable)
        if code == 2:
            if not is_master_key(api_key):
                return redirect("/interface/message/?api_key="+str(api_key)+"&cup_id="+str(cup_id)+"&message[]=Cup%20is%20already%20registered")
            return HttpResponse("already registered")
        elif code == 1:
            if not is_master_key(api_key):
                return redirect("/interface/message/?api_key="+str(api_key)+"&cup_id="+str(cup_id)+"&message[]=Successfully%20registered%20cup%20with%20id " + str(cup_id) + "%20.")
            return HttpResponse("successfully registered")
        else:
            if not is_master_key(api_key):
                return redirect("/interface/message/?api_key="+str(api_key)+"&cup_id="+str(cup_id)+"&message[]=Error%20while%20saving%20to%20database")
            return HttpResponse("database error")

    elif action == '2':
        cup_id = request.GET.get("cup_id", "")
        if check_cup_id(cup_id):
            code = delete_cup(cup_id)
            if code == 1:
                return redirect("/interface/message/?api_key="+str(api_key)+"&cup_id="+str(cup_id)+"&message[]=Successfully%20deleted%20cup%20with%20id%20" + str(cup_id) + "%20.")
            elif code == 2:
                return redirect("/interface/message/?api_key="+str(api_key)+"&cup_id="+str(cup_id)+"&message[]=Cup%20with%20id%20" + str(cup_id) + "%20does%20not%20exist")
            else:
                return redirect("/interface/message/?api_key="+str(api_key)+"&cup_id="+str(cup_id)+"&message[]=Error%20while%20deleting%20from%20database")
        else:
            return redirect("/interface/message/?api_key="+str(api_key)+"&cup_id="+str(cup_id)+"&message[]=Ungültiger%20Becher!")

    elif action == '3':
        cup_id = request.GET.get("cup_id", "")
        drink_name = request.GET.get("drink_name", "")
        if check_cup_id(cup_id):
            order = request.GET.getlist("order[]")
            if order:
                order_string = ""
                counter = 0
                for o in order:
                    if counter % 2:
                        order_string += str(o) + ";"
                        counter += 1
                    else:
                        order_string += str(o) + ":"
                        counter += 1
                if place_order(cup_id, order_string):
                    return redirect("/interface/message/?api_key="+str(api_key)+"&cup_id="+str(cup_id)+"&drink_name="+str(drink_name)+"&message[]=Bestellung%20für%20Becher%20" + str(cup_id) + "%20erfolgreich%20aufgegeben!")
                return redirect("/interface/message/?api_key="+str(api_key)+"&cup_id="+str(cup_id)+"&drink_name="+str(drink_name)+"&message[]=Fehler%20beim%20Aufgeben%20der%20Bestellung!")
            else:
                return redirect("/interface/message/?api_key="+str(api_key)+"&cup_id="+str(cup_id)+"&drink_name="+str(drink_name)+"&message[]=Bestellung%20fehlt!")
        else:
            return redirect("/interface/message/?api_key="+str(api_key)+"&cup_id="+str(cup_id)+"&drink_name="+str(drink_name)+"&message[]=Ungültiger%20Becher!")

    elif action == '4':
        cup_id = request.GET.get("cup_id", "")
        if check_cup_id(cup_id):
            enc = False
            prep = False
            if is_master_key(api_key):
                enc = True
                prep = True
            order = get_order(cup_id, encoded=enc, prepare_drink=prep)
            if order:
                if enc:
                    return HttpResponse(order)
                return redirect("/interface/message/?api_key="+str(api_key)+"&cup_id="+str(cup_id)+"&message[]=" + order + "%20was%20successfully%20prepared")
            return redirect("/interface/message/?api_key="+str(api_key)+"&cup_id="+str(cup_id)+"&message[]=There%20is%20no%20order%20for%20cup%20" + str(cup_id))
        else:
            return redirect("/interface/message/?api_key="+str(api_key)+"&cup_id="+str(cup_id)+"&message[]=Ungültiger%20Becher!")

    elif action == '5':
        if is_master_key(api_key):
            key = gen_api_key()
            return redirect("/interface/message/?api_key="+str(api_key)+"&cup_id="+str(cup_id)+"&message[]=API%20key%20is%20" + key)
        return redirect("/interface/message/?api_key="+str(api_key)+"&cup_id="+str(cup_id)+"&message[]=You%20are%20not%20authorized%20to%20generate%20API%20keys")

    elif action == '6':
        cup_id = request.GET.get("cup_id", "")
        file_name = gen_qr_code("http://mrbartender.cloud/?api_key=" + gen_api_key() + "&cup_id=" + str(cup_id))
        img = open(file_name, "rb")
        return FileResponse(img)

    elif action == '7':
        if not is_master_key(api_key):
            return redirect("/interface/message/?api_key="+str(api_key)+"&cup_id="+str(cup_id)+"&message[]=You%20are%20not%20authorized&20to%20perform%20this&20action")
        cup_id = request.GET.get("cup_id", "")
        if not check_cup_id(cup_id):
            register_cup(cup_id, mixable=True)
            return HttpResponse("Successfully registered cup with ID " + cup_id)
        else:
            order = get_order(cup_id, encoded=True, prepare_drink=True)
            if not order == "0:::::::::::0000":
                return HttpResponse(order)
            return HttpResponse("There is no order registered for this cup")

    else:
        return redirect("/interface/message/?api_key="+str(api_key)+"&cup_id="+str(cup_id)+"&message[]=invalid%20action%20code")

