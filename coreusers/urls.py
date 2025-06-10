from django.contrib import admin
from django.urls import path, include
from . import views
app_name = "coreusers"

urlpatterns = [
    path("user/panel/",views.UserPanelView.as_view(),name="user-panel"),

]