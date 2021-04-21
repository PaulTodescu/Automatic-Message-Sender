from django.db import models
from list.models import List
from message.models import Message


class Campaign(models.Model):
    title = models.CharField(max_length=50, verbose_name="Title")
    list = models.ForeignKey(List, on_delete=models.SET_NULL, null=True)
    message = models.ForeignKey(Message, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
