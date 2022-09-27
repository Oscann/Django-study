from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect
import json
import requests

from api.models import Block, Users

# Create your views here.


def home(req):
    id = req.COOKIES.get("AuthToken")

    user = Users.objects.get(id=id)
    if req.method == "POST":
        name = req.POST.get("name")
        user.page_set.create(name=name)

    pages = user.page_set.all()

    return render(req, "main/home.html", {"pages": pages, "user": user})


def sign_up(req):
    if req.method == "POST":
        print("start")
        data = req.POST
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        print("userdata fetched")
        r = requests.post(url="http://127.0.0.1:8000/api/sign-up/",
                          data=json.dumps({"username": username, "password": password, "email": email}))
        return HttpResponseRedirect(redirect_to="/login/", content=r.content, headers=r.headers)
    return render(req, "main/sign-up.html")


def login(req):
    if req.method == "POST":
        data = req.POST
        username = data.get("username")
        password = data.get("password")
        r = requests.post(url="http://127.0.0.1:8000/api/login/",
                          data=json.dumps({"username": username, "password": password}))
        print(r.cookies)
        return HttpResponseRedirect(redirect_to="/", content=r.content, headers=r.headers)
    return render(req, "main/login.html")


def page(req, username, page_id):

    user = Users.objects.get(username=username)
    page = user.page_set.get(id=page_id)
    blocks = page.block_set

    if req.method == "POST":
        if req.POST.get("save"):

            if (req.POST.get("in_text")):
                content = req.POST.get("in_text")
                blocks.create(content=content, priority=len(
                    blocks.all()) + 1, page_id=page.id)

            for block in blocks.all():
                print(block)
                if req.POST.get(str(block.id)) != block.content:
                    block.content = req.POST.get(str(block.id))
                    try:
                        block.save()
                    except:
                        print("Unexistent block")
            return HttpResponseRedirect(req.path)

        elif req.POST.get("delete"):
            id = req.POST.get("delete")[7:]

            if blocks.filter(id=id):
                blocks.get(id=id).delete()

            return HttpResponseRedirect(req.path)

    blocks = blocks.all().order_by("priority")

    return render(req, "main/page.html", {"blocks": blocks.all(), "page": page})
