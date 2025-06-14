from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, exceptions
from ...models import Note
from coreusers.models import CustomUser



class NoteSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(queryset=CustomUser.objects.all(),slug_field="email")
    class Meta:
        model = Note
        fields = ["id","title","content","created_by","created_date"]