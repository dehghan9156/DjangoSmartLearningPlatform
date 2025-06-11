from django.contrib.messages import success
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from DjangoSmartLearningPlatform.settings import OPENAI_API_KEY
import requests
from django.http import JsonResponse
from django.conf import settings
import openai
from datetime import timedelta
import logging
from django.views import View

class HomeView(View):
    def get(self,request):
        return render(request,"home.html")