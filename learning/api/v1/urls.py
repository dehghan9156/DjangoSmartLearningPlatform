from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "api-v1"

urlpatterns = [
    path("note/read/", views.NoteReadApiView.as_view(), name="note-read"),
]
