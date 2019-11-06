"""
Define app serializers.
"""

from rest_framework import serializers
from wordcount.models import FileUpload


class FileUploadSerializer(serializers.ModelSerializer):
    """
    Serializer for a collection of file upload results.
    """
    class Meta:
        model = FileUpload
        exclude = ['words']
        read_only_fields = ['__all__']


class FileUploadSerializerSingle(serializers.ModelSerializer):
    """
    Serializer for a single file upload result.
    """
    class Meta:
        model = FileUpload
        fields = '__all__'
        read_only_fields = ['__all__']
