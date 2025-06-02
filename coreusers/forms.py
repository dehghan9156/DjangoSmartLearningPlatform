from django import forms
from allauth.account.forms import SignupForm as AllauthSignupForm

class CustomSignupForm(AllauthSignupForm):
    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    def save(self, request):
        user = super().save(request)
        user.role = self.cleaned_data["role"]
        user.save()
        return user
