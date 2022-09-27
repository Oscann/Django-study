from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login, name="login"),
    path("sign-up/", views.sign_up, name="sign-up"),
    path("", views.home, name="home"),
    path("page/<str:username>/<int:page_id>/", views.page, name="page")
]
