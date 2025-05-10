from django.contrib import admin
from .models import Note
from django.contrib.admin import ModelAdmin


class CustomNote(ModelAdmin):
    list_display = ("title","content","created_by","created_date",)
    search_fields = ("id",)

admin.site.register(Note,CustomNote)