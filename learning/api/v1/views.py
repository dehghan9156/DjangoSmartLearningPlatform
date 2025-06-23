from http.client import responses
from django.conf import settings
from django.core.serializers import serialize
from django.db.models.fields import return_None
from django.shortcuts import get_object_or_404
from django.template.context_processors import request
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from rest_framework.generics import CreateAPIView,GenericAPIView
from .serialization import *
from ...models import *
from .permissions import IsTeacherPermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
import requests


class NoteReadApiView(generics.ListAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permissions = IsAuthenticated
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id']
    search_fields = ['id', 'title', 'content']
    order_fields = ['id']


class NoteDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsTeacherPermission]


class NoteSummaryApiView(APIView):
    def post(self, request, pk):
        try:
            note = Note.objects.get(pk=pk)
        except Note.DoesNotExist:
            return Response({"error": "note does not exit."}, status=status.HTTP_404_NOT_FOUND)

        try:
            summary = self.call_deepseek(note.content)
            return Response(summary, status=status.HTTP_200_OK)
        except ConnectionError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def call_deepseek(self, prompt):
        url = "https://api.openai.com/v1/chat/completions"
        api_key = settings.OPENAI_API_KEY
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user",
                          "content": f"Please summarize this text in the same language as the input:\n{prompt}"}],
            "temperature": 0.7
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()  # اگر وضعیت 4xx یا 5xx باشه خطا می‌ندازه
            result = response.json()

            if "choices" in result:
                return result["choices"][0]["message"]["content"]
            else:
                return "⚠️ Unexpected response from DeepSeek."
        except Exception as e:
            return f"❌ Error communicating with DeepSeek: {str(e)}"


class NoteCreateQuestionGPTApiView(APIView):
    def post(self,request,pk):
        try:
            note = Note.objects.get(pk=pk)
        except Note.DoesNotExist:
            return Response({"messages": "note does not exist"},status=status.HTTP_404_NOT_FOUND)
        try:
            lst_question = []
            questions_text = self.call_deepseek(note.content)
            # print("question_text",questions_text)
            blocks = questions_text.strip().split('\n\n')
            # print("blocks",blocks)
            for block in blocks:
                que=block.strip().split('\n')
                lst_question.append(que)
            return Response({"questions":lst_question,"messages":"question successfully created."},status=status.HTTP_200_OK)
        except ConnectionError:
            return Response({"messages":"connection failed.sorry"},status=status.HTTP_503_SERVICE_UNAVAILABLE)
        
    def call_deepseek(self, prompt):
        url = "https://api.openai.com/v1/chat/completions"
        api_key = settings.OPENAI_API_KEY
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-4o-mini",
            "messages": [{
                "role": "user",
                "content": f"""The following is a user note:
                        ---
                        {prompt}
                        ---


                        Based on the above note, generate four multiple-choice test questions. For each question:
                        - Provide four options labeled A, B, C, and D.
                        - Clearly indicate the correct answer at the end of each question in the format: Answer: X (e.g., Answer: B)
                        - Do not provide any explanation or reasoning.

                        Output format:
                        1. [Question text]
                        A) ...
                        B) ...
                        C) ...
                        D) ...
                        Answer: [correct option letter]
                        ...
                        """
            }],

            "temperature": 0.7
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()  # اگر وضعیت 4xx یا 5xx باشه خطا می‌ندازه
            result = response.json()

            if "choices" in result:
                return result["choices"][0]["message"]["content"]
            else:
                return "⚠️ Unexpected response from DeepSeek."
        except Exception as e:
            return f"❌ Error communicating with DeepSeek: {str(e)}"

class NoteAskQuestionGptApiView(generics.GenericAPIView):
    serializer_class = QuestionNoteSerializer
    def post(self,request,pk):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try :
                note = Note.objects.get(pk=pk)
                question = serializer.validated_data['question']
                ans_gpt = self.call_deepseek(question,note)
                return Response(ans_gpt,status=status.HTTP_200_OK)
            except Note.DoesNotExist:
                return Response(status=status.HTTP_501_NOT_IMPLEMENTED)
        else:
            print({"message":"serializer is not valid."})
     
        
    def call_deepseek(self, question, prompt):
        url = "https://api.openai.com/v1/chat/completions"
        api_key = settings.OPENAI_API_KEY
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-4o-mini",
            "messages": [{
                "role": "user",
                "content": f"""The following is a user note:
                    ---
                    {prompt}
                    ---
                    
                    Now, answer this question based **only** on the content above:
                    {question}
                    """
            }],

            "temperature": 0.7
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()  # اگر وضعیت 4xx یا 5xx باشه خطا می‌ندازه
            result = response.json()

            if "choices" in result:
                return result["choices"][0]["message"]["content"]
            else:
                return "⚠️ Unexpected response from DeepSeek."
        except Exception as e:
            return f"❌ Error communicating with DeepSeek: {str(e)}"


class ExamSelectApiView(generics.RetrieveAPIView):
    def get(self,request,pk):
        question = Question.objects.filter(note=pk)
        permissions =IsAuthenticated
        serializer = QuestionSerializer(question,many=True)
        return Response(serializer.data)   

    
