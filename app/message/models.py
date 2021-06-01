from django.db import models


class Message(models.Model):
    title = models.CharField(max_length=50)
    diff_gender = models.BooleanField(null=True)
    message = models.TextField(max_length=500)
    csv_fields = models.FileField(upload_to='uploads/message_fields')
    html = models.BooleanField(default=False)

    def __str__(self):
        return self.title
