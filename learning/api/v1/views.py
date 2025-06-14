from http.client import responses
import jwt
from django.conf import settings
from django.core.serializers import serialize
from django.shortcuts import get_object_or_404
from django.template.context_processors import request
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from rest_framework.generics import CreateAPIView


