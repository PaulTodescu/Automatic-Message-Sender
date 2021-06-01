from django.db import models

gender = (
    ("M", "M"),
    ("F", "F"),
)

class Person(models.Model):
    name = models.CharField(max_length=120)
    gender = models.CharField(max_length=2, choices=gender, default="")
    phone = models.CharField(max_length=12, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=12, unique=True, null=True, blank=True)

    def __str__(self):
        return self.name
