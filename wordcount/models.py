"""
Define app models.
"""

from django.db import models
from django.contrib.postgres.fields import JSONField


class FileUpload(models.Model):
    """Model for a file upload object"""
    created = models.DateTimeField(auto_now_add=True)
    # file = models.FileField()
    wordcount = models.IntegerField()
    words = JSONField()
    lines = models.IntegerField()
