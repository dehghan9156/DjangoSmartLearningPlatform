from django.contrib.messages import success
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from DjangoSmartLearningPlatform.settings import OPENAI_API_KEY
from .forms import *
from .models import *
import requests,json
from django.http import JsonResponse
from django.conf import settings
import openai
from datetime import timedelta
import logging
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils import timezone
from learning.models import *


class UserPanelView(View):
    def get(self, request):
        exam_feedback = ExamAnswer.objects.filter(student=request.user)
        lst_score = []
        lst_labels = []
        for sc in exam_feedback:
            lst_score.append(sc.score)
            lst_labels.append(sc.note.title)
        max_score = max(lst_score)
        min_score = min(lst_score)
        context = {
            'labels':json.dumps(lst_labels),
            'scores':json.dumps(lst_score)
        }
        return render(request, "coreusers/user_panel.html",{
                        "exam_feedback": exam_feedback,
                       "max_score": max_score,
                       "min_score": min_score,
                       "lst_labels": lst_labels,
                       "lst_score": lst_score,**context})
