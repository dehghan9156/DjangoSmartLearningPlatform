from django.db import models
from accounts.models import CustomUser
from accounts.models import CustomUser

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
