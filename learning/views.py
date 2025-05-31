from django.contrib.messages import success
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from DjangoSmartLearningPlatform.settings import OPENAI_API_KEY
from .forms import *
from .models import *
import requests
from django.http import JsonResponse
from django.conf import settings
import openai


class NoteAddView(View, LoginRequiredMixin):
    def get(self, request):
        form = NoteForm()
        return render(request, "learning/note-add.html", {"form": form})

    def post(self, request):
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.created_by = request.user
            note.save()
            messages.success(request, "Note create successfully.", "success")
            return redirect("learning:note-list")
        return render(request, "learning/note-add.html", {"form": form})


class NoteListView(View, LoginRequiredMixin):
    def get(self, request):
        notes = Note.objects.filter(created_by=self.request.user)
        if notes.exists():
            return render(request, "learning/note-list.html", {"notes": notes})
        return render(request, "learning/note-list.html", {"messages": "There are no notes for you."})


class NoteDeleteView(View, LoginRequiredMixin):
    def get(self, request, pk):
        note = Note.objects.get(pk=pk)
        note.delete()
        messages.success(request, "your note has successfully.", "success")
        return redirect("learning:note-list")


class NoteUpdateView(View, LoginRequiredMixin):
    def get(self, request, pk):
        note = Note.objects.get(pk=pk)
        form = NoteForm(instance=note)
        return render(request, "learning/note-update.html", {"form": form})

    def post(self, request, pk):
        note = Note.objects.get(pk=pk)
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, "your note updated successfully", 'success')
            return redirect("learning:note-list")
        messages.error(request, "your form is not valid.", 'danger')
        return render(request, "learning/note-update.html", {"form": form})


class TestView(View):
    def get(self, request):
        return render(request, 'learning/websocket.html')


class GptSummaryView(View):
    def get(self, request, pk):
        note_id = pk
        note = None
        summary = None
        if note_id:
            try:
                note = Note.objects.get(id=note_id)
                summary = self.call_deepseek(note.content)
                print(note)
            except Note.DoesNotExist:
                summary = "❌ Note not found."

        return render(request, "learning/note-summary-gpt.html", {
            "note": note,
            "summary": summary
        })

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


class GptNotQuestionView(View):
    def get(self, request, pk):
        form = QuestionNoteForm()
        return render(request, "learning/note-question-gpt.html", {"form": form})

    def post(self, request, pk):
        form = QuestionNoteForm(request.POST)
        answer = None
        note = Note.objects.get(pk=pk)
        if form.is_valid():
            question = form.cleaned_data["question"]
            answer = self.call_deepseek(question, note.content)
        return render(request, "learning/note-question-gpt.html", {"form": form, "answer": answer, "note": note})

    def call_deepseek(self, question, prompt):
        url = "https://api.openai.com/v1/chat/completions"
        api_key = OPENAI_API_KEY
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


class NoteDetailView(View):
    def get(self, request, pk):
        note = Note.objects.get(pk=pk)
        return render(request, "learning/note-detail.html", {"note": note})


class NoteCreateQuestionbyGptView(View):
    def post(self, request, pk):
        save_question = []
        note = Note.objects.get(pk=pk)
        prompt = note.content
        # 1. دریافت خروجی خام از GPT
        question_text = self.call_deepseek(prompt)

        # 2. تبدیل به لیست خطوط (خط‌به‌خط)
        question_list = [line.strip() for line in question_text.strip().split("\n") if line.strip()]

        # 3. ساختاردهی هر 5 خط (سؤال و گزینه‌ها) به دیکشنری
        structured_questions = []
        for i in range(0, len(question_list), 6):  # چون الان 6 خط برای هر سؤال داریم
            try:
                answer_line = question_list[i + 5]
                answer_letter = answer_line.replace("Answer:", "").strip()

                q = {
                    "question": question_list[i],
                    "A": question_list[i + 1],
                    "B": question_list[i + 2],
                    "C": question_list[i + 3],
                    "D": question_list[i + 4],
                    "answer": answer_letter  # اضافه شدن گزینه صحیح
                }
                structured_questions.append(q)
            except IndexError:
                print(f"⚠️ Skipping incomplete question block at index {i}")

        # 4. ارسال همه چیز به قالب
        return render(request, "learning/note-question-by-gpt.html", {
            "note": note,
            "question_text": question_text,
            "question_list": question_list,
            "structured_questions": structured_questions
        })

    def call_deepseek(self, prompt):
        url = "https://api.openai.com/v1/chat/completions"
        api_key = OPENAI_API_KEY
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


class NoteCheckAnswerGptView(View):
    def post(self, request, pk):
        note = Note.objects.get(pk=pk)
        answers = request.POST
        # print(answers)
        lst_ans = []
        for key in answers:
            if key.startswith("answer_"):
                ans_user = answers[key]
                lst_ans.append(ans_user)
        print(lst_ans)

        feedback = self.call_deepseek(note, lst_ans)
        print("پرومپت نهایی:\n", note)
        print("پاسخ کامل GPT:\n", feedback)
        return render(request, "learning/feedback-gpt.html",
                      {"lst_ans": lst_ans, "feedback": feedback})

    def call_deepseek(self, note, lst_ans):
        url = "https://api.openai.com/v1/chat/completions"
        api_key = OPENAI_API_KEY
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # 🧠 ساخت پرامپت قابل درک برای GPT
        prompt = f"""The following is a user note:
        ---
        {note.content}
        ---

        The following are multiple answers based ONLY on the note above.
        Please evaluate EACH answer separately.

        For each answer, indicate if it is correct ✅ or incorrect ❌ and explain why.

        """

        for i, answer in enumerate(lst_ans, 1):
            prompt += f"\nAnswer {i}: {answer}"

        data = {
            "model": "gpt-4o-mini",
            "messages": [{
                "role": "user",
                "content": prompt
            }],
            "temperature": 0.5
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()

            if "choices" in result:
                return result["choices"][0]["message"]["content"]
            else:
                return "⚠️ Unexpected response from GPT."
        except Exception as e:
            return f"❌ Error communicating with GPT: {str(e)}"
