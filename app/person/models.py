from django.db import models

gender = (
    ("M", "M"),
    ("F", "F"),
)


class Person(models.Model):
    name = models.CharField(max_length=120, verbose_name='Name')
    gender = models.CharField(max_length=2, choices=gender, default="", verbose_name='Gender')
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True, verbose_name='Phone')
    email = models.EmailField(max_length=100, unique=True, null=True, blank=True, verbose_name='Email')

    def __str__(self):
        return self.name
