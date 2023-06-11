from django.db import models


class User(models.Model):
    id = models.UUIDField()
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    discord_nick = models.CharField(max_length=30)
    email = models.EmailField()

class Book(models.Model):
    id = models.UUIDField()
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50)
    summary = models.TextField(max_length=1000)
    tags = models.ManyToManyField("Tag")
    proposer = models.OneToOneField(User, on_delete=models.SET_NULL)
    readers = models.ManyToManyField(User)

class Tag(models.Model):
    id = models.UUIDField()
    name = models.CharField(max_length=50)