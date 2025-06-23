from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, exceptions
from ...models import Note,Question
from coreusers.models import CustomUser



class NoteSerializer(serializers.ModelSerializer):
    created_by = serializers.SlugRelatedField(queryset=CustomUser.objects.all(),slug_field="email")
    class Meta:
        model = Note
        fields = ["id","title","content","created_by","created_date"]


class QuestionNoteSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=200)


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        # fields = ['pk','soal','correct_answer']
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        # print(rep)
        rep.pop('correct_answer')
        return rep
