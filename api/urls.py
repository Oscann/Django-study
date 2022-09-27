from django.urls import path
from .views import auth, createUser

urlpatterns = [
    path("login/", auth),
    path("sign-up/", createUser)
]
