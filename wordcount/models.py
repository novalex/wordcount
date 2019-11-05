from django.db import models


class FileUpload(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    data = models.FileField()
