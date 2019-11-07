"""
Define app views.
"""

import re
from rest_framework import views
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from wordcount.settings import WORDCOUNT_API
from wordcount.models import FileUpload
from wordcount.serializers import FileUploadSerializer, FileUploadSerializerSingle
from wordcount.functions import check_spelling


class FileUploadView(views.APIView):
    """
    Handle uploading files, processing and fetching results.
    """
    parser_classes = [FileUploadParser]

    def process_file(self, file_obj, request):
        """
        Handles processing the file and counting words.
        Returns dict of data or false if no valid ASCII lines were found.
        """
        line_nr = 0
        wordcount = 0
        words = {}
        error_lines = []
        found_text = False
        skip_word = False if 'skip_words_containing' not in request.GET else request.GET['skip_words_containing']

        # Read lines
        for line in file_obj:
            line_nr += 1

            # Validate ASCII
            try:
                line = line.decode('ascii')
                found_text = True
            except UnicodeDecodeError:
                # Could not decode current line, mark the line and skip to next line
                error_lines.append(line_nr)
                continue

            # Remove undesirable characters from line
            line = re.sub(r'[^a-zA-Z0-9\s\-\'@\.,\\/]', '', line)
            # Split line into individual words
            words_now = line.split()
            for word in words_now:
                # Convert all words to lowercase in order to keep count consistently
                word_lc = word.lower()
                # Remove trailing commas, periods, slashes
                word_lc = word_lc.rstrip(',./\'')
                # Check if we still have a word, skip if not
                if not word_lc:
                    continue
                # Skip words containing specified value if the query arg is set
                if skip_word and skip_word in word_lc:
                    continue
                # Increment current word count
                if word_lc in words:
                    words[word_lc] += 1
                else:
                    words[word_lc] = 1
                # Increment total word count
                wordcount += 1

        # No valid ASCII text found in the file
        if not found_text:
            return False

        if 'check_spelling' in request.GET:
            words['misspelled_words'] = check_spelling(' '.join(words))

        return {
            'wordcount': wordcount,
            'words': words,
            'lines': line_nr,
            'error_lines': error_lines
        }

    def get(self, request):
        """
        Returns a list of all existing wordcount records.
        """
        if 'id' in request.GET:
            try:
                result = FileUpload.objects.get(id=request.GET.get('id'))
            except FileUpload.DoesNotExist:
                return Response({
                    'error': 'No result found with specified id.'
                }, 404)
            serialized = FileUploadSerializerSingle(result)
        else:
            serialized = FileUploadSerializer(
                FileUpload.objects.all(), many=True)

        return Response(serialized.data, 200)

    def post(self, request):
        """
        Handles validating and processing uploaded file and saving information to database.
        """
        # Check if a file exists in the request data
        if not 'file' in request.data:
            return Response({
                'error': 'No file uploaded.'
            }, 400)

        file_obj = request.data['file']

        # Validate maximum filesize
        if file_obj.size > WORDCOUNT_API['MAX_FILESIZE']:
            max_size_mb = (WORDCOUNT_API['MAX_FILESIZE'] / 1000000)
            return Response({
                'error': 'Uploaded file is too large, limit is %d MB' % max_size_mb
            }, 413)

        data = self.process_file(file_obj, request)

        if not data:
            # File could not be processed
            return Response({
                'error': 'File does not contain valid ASCII text, possibly corrupted or not a text file.'
            }, 400)

        # Save results to DB
        file = FileUpload(
            wordcount=data['wordcount'],
            words=data['words'],
            lines=data['lines']
        )
        file.save()

        # Create response object
        resp = {
            'id': file.id,
            'wordcount': data['wordcount'],
            'words': data['words'],
            'lines': data['lines'],
        }

        # Lines with errors were encountered
        if data['error_lines']:
            resp['error'] = '%d lines could not be parsed as valid ASCII and have been skipped.' % len(data['error_lines'])

        return Response(resp, 200)
