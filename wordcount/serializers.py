from rest_framework import serializers
from wordcount.models import FileUpload


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        exclude = ['words']
        read_only_fields = ['__all__']

class FileUploadSerializerSingle(serializers.ModelSerializer):
    class Meta:
        model = FileUpload
        fields = '__all__'
        read_only_fields = ['__all__']
