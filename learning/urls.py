from django.contrib import admin
from django.urls import path,include
from . import views


app_name ="learning"

urlpatterns = [
    path("note/add/",views.NoteAddView.as_view(),name="note-add"),
    path("note/list/",views.NoteListView.as_view(),name="note-list"),
    path("note/delete/<int:pk>/",views.NoteDeleteView.as_view(),name="note-delete"),
    path("note/update/<int:pk>/",views.NoteUpdateView.as_view(),name="note-update")
]
