from django.db import models
import datetime

from person.models import Person

list_types = (
    ("Phone", "Phone"),
    ("Email", "Email"),
    ("Mixt", "Mixt"),
)


class List(models.Model):
    name = models.CharField(max_length=100, default="", verbose_name='Name')
    date = models.DateField(auto_now=False, default=datetime.date.today)
    reason = models.TextField(default="")
    type = models.CharField(max_length=20, choices=list_types, default="")
    people = models.ManyToManyField(Person, blank=True)
    csv_file = models.FileField(upload_to='uploads/people_lists', null=True, blank=True)

    def __str__(self):
        return self.name
