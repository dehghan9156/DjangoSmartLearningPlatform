from django.contrib.messages import success
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .forms import *
from .models import *



class NoteAddView(View,LoginRequiredMixin):
    def get(self,request):
        form = NoteForm()
        return render(request,"learning/note-add.html",{"form":form})

    def post(self,request):
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.created_by = request.user
            note.save()
            messages.success(request,"Note create successfully.","success")
            return redirect("learning:note-list")
        return render(request,"learning/note-add.html",{"form":form})

class NoteListView(View,LoginRequiredMixin):
    def get(self,request):
        notes = Note.objects.filter(created_by=self.request.user)
        if notes.exists():
            return render(request,"learning/note-list.html",{"notes":notes})
        return render(request,"learning/note-list.html",{"messages":"There are no notes for you."})
