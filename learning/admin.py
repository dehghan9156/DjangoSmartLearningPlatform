from django.contrib import admin
from .models import *
from django.contrib.admin import ModelAdmin


class CustomNote(ModelAdmin):
    list_display = ("title","content","created_by","created_date",)
    search_fields = ("id",)


class CustomMessage(ModelAdmin):
    list_display = ("sender","reciver","message_txt","time",)
    search_fields = ("id",)


class CustomQuestion(ModelAdmin):
    list_display = ("note","pk","correct_answer",)
    search_fields = ("id",)

admin.site.register(Note,CustomNote)
admin.site.register(Message,CustomMessage)
admin.site.register(Question,CustomQuestion)