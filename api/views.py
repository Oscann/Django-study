from datetime import timedelta
import json
from webbrowser import get
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from .models import Users
import requests
from .utils import parsePost

# Create your views here.


@csrf_exempt
def createUser(req):
    data = req.body
    print(data)
    data = data.decode("utf-8")
    if (req.POST):
        data = parsePost(data)
    body = json.loads(data)

    query_1 = list(Users.objects.filter(email=body["email"]))
    query_2 = list(Users.objects.filter(username=body["username"]))

    if (len(query_1) == 0 and len(query_2) == 0):
        Users.objects.create(
            username=body["username"], email=body["email"], password=body["password"])
        return JsonResponse(data={"success": True})
    return JsonResponse(data={"success": False})


@csrf_exempt
def auth(req):
    data = req.body.decode("utf-8")

    if (req.POST):
        data = parsePost(data)
    body = json.loads(data)
    print("After json")
    try:
        user = Users.objects.get(username=body["username"])

        if (body["password"] == user.password):
            print("Start cookie production, yummy!!!!")
            res = JsonResponse(data={"success": True})
            res.set_cookie(key="AuthToken", value=user.id,
                           samesite="strict", max_age=100000,
                           httponly=True, secure=True)
            print("Sending cookie...")
            return res
        else:
            print("Access Denied")
    except Exception:
        print("Error")

    return JsonResponse(data=body)
