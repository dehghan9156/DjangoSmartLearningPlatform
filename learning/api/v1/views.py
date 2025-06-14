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
from .serialization import *
from ...models import *
from .permissions import IsTeacherPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class NoteReadApiView(generics.ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permissions = IsAuthenticated
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['id']
    search_fields = ['id','title','content']
    order_fields = ['id']

class NoteDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes  = [IsTeacherPermission]

