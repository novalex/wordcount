from rest_framework import serializers
from wordcount.models import FileUpload


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        exclude = ['words', 'extra']
        read_only_fields = ['__all__']
