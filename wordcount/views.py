import json
from wordcount import settings
from rest_framework import views
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser


class FileUploadView(views.APIView):
    parser_classes = [FileUploadParser]

    def put(self, request, format=None):
        file_obj = request.data['file']

        if file_obj.size > settings.WORDCOUNT_API['MAX_FILESIZE']:
            resp = {
                'error': 'Uploaded file is too large, limit is %d MB' % (settings.WORDCOUNT_API['MAX_FILESIZE'] / 1000000)
            }
            return Response(resp, 413)

        resp = {
            'wordcount': 0,
            'words': {},
            'file': {
                'name': file_obj.name,
                'size': file_obj.size,
            }
        }

        return Response(resp, 200)
