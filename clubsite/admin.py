from django.contrib import admin

from .models import (
    User, Book, Meeting, Post, Tag
)

# Register your models here.
for model in [
    User,
    Book,
    Meeting,
    Post,
    Tag
]:
    admin.site.register(model)
