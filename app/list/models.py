from django.db import models
import datetime

list_types = (
    ("Phone", "Phone"),
    ("Email", "Email"),
    ("Mixt", "Mixt"),
)


class List(models.Model):
    name = models.CharField(max_length=100, default="", verbose_name='Name')
    date = models.DateField(auto_now=False, default=datetime.date.today)
    reason = models.TextField(default="")
    type = models.CharField(max_length=100, choices=list_types, default="")
    csv_file = models.FileField(upload_to='uploads/people_lists')

    def __str__(self):
        return self.name
