from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title","content"]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'content': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }

class QuestionNoteForm(forms.Form):
    question = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "style": "color: black; background-color: white;",
            "placeholder": "Ask your question?"
        })
    )
