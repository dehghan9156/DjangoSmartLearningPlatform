from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "api-v1"

urlpatterns = [
    path("note/read/", views.NoteReadApiView.as_view(), name="note-read"),
    path("note/detail/<int:pk>/",views.NoteDetailApiView.as_view(),name="note-detail"),
    path("note/summary/<int:pk>/",views.NoteSummaryApiView.as_view(),name="note-summary"),
    path("note/question/by/gpt/<int:pk>/",views.NoteQuestionGPTApiView.as_view(),name="note-question"),
]
