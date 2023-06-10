from django.urls import path, URLPattern
from . import views

from typing import List


urlpatterns: List[URLPattern] = [
    path("", views.index, name="index"),
]