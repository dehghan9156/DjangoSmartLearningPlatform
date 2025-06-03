from django.db import models
from coreusers.models import CustomUser
from coreusers.models import CustomUser

class Note(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    created_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    sender = models.ForeignKey(CustomUser,related_name="sender",on_delete=models.CASCADE)
    reciver = models.ForeignKey(CustomUser,related_name="reciver",on_delete=models.CASCADE)
    message_txt = models.TextField(max_length=250)
    time = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    note = models.ForeignKey(Note,on_delete=models.CASCADE)
    soal = models.TextField(max_length=250)
    correct_answer = models.CharField(max_length=250)
    option_a = models.CharField(max_length=250)
    option_b = models.CharField(max_length=250)
    option_c = models.CharField(max_length=250)
    option_d = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.note.title}--{self.pk}"

class ExamAnswer(models.Model):
    student = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    exam = models.ForeignKey(Note,on_delete=models.CASCADE)
    score = models.IntegerField()
    created_data = models.DateTimeField(auto_now_add=True)