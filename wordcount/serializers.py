from rest_framework import serializers
from wordcount.models import FileUpload


class FileUploadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FileUpload
        read_only_fields = '__all__'
