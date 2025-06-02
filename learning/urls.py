from django.contrib import admin
from django.urls import path,include
from . import views
app_name ="learning"

urlpatterns = [
    path("note/add/",views.NoteAddView.as_view(),name="note-add"),
    path("note/list/",views.NoteListView.as_view(),name="note-list"),
    path("note/delete/<int:pk>/",views.NoteDeleteView.as_view(),name="note-delete"),
    path("note/update/<int:pk>/",views.NoteUpdateView.as_view(),name="note-update"),
    path("test/",views.TestView.as_view(),name="test"),
    path("summary/gpt/<int:pk>/",views.GptSummaryView.as_view(),name="summary-gpt"),
    path("note/question/gpt/<int:pk>/",views.GptNotQuestionView.as_view(),name="note-question-gpt"),
    path("note/detail/<int:pk>/",views.NoteDetailView.as_view(),name="note-detail"),
    path("note/create/question/<int:pk>/",views.NoteCreateQuestionbyGptView.as_view(),name="create-question-by-gpt"),
    path("note/check/answer/<int:pk>/",views.NoteCheckAnswerGptView.as_view(),name="note-check-answer-gpt"),
    path("exam/read/",views.ExamReadyView.as_view(),name="exam-ready"),
]

