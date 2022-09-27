
from django.db import models

# Create your models here.


class Users(models.Model):
    username = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.username

class Page(models.Model):
    pages = models.Manager()
    name = models.CharField(max_length=30)
    user = models.ForeignKey("Users", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

class Block(models.Model):
    content = models.TextField()
    priority = models.IntegerField()

    page = models.ForeignKey("Page", on_delete=models.CASCADE)

    def __str__(self):
        return self.content + ": " + str(self.priority)