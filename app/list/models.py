from django.db import models

import datetime


# Create your models here.

list_types = (
    ("1","Phone"),
    ("2","Email"),
    ("3","Mixt"),
)


class List(models.Model):
    name = models.CharField(max_length=100, default="")
    date = models.DateField(auto_now=False, default=datetime.date.today)
    reason = models.TextField(default="")
    type = models.CharField(max_length=100, choices=list_types, default="")

    def __str__(self):
        return self.name

