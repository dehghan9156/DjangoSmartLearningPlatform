from django.db import models
from accounts.models import CustomUser


class Note(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField(max_length=250)
    created_by = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)