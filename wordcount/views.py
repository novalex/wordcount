from wordcount import settings
from wordcount.models import FileUpload
from rest_framework import views
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
import re


class FileUploadView(views.APIView):
    parser_classes = [FileUploadParser]

    def validate_filesize(self, size):
        """
        Validates given file size (in bytes) against maximum allowed value set in settings.
        """
        if size > settings.WORDCOUNT_API['MAX_FILESIZE']:
            resp = {
                'error': 'Uploaded file is too large, limit is %d MB' % (settings.WORDCOUNT_API['MAX_FILESIZE'] / 1000000)
            }
            return Response(resp, 413)

    def process_file(self, file_obj):
        """
        Handles validating and parsing file.
        """
        # Validate maximum filesize
        self.validate_filesize(file_obj.size)

        # Read lines
        line_nr = 0
        wordcount = 0
        words = {}
        error_lines = []
        found_text = False
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

            # Get words
            words_now = re.sub(r'[^a-zA-Z\s]', '', line).split()
            for word in words_now:
                word_lc = word.lower() # Convert all words to lowercase in order to keep count
                if word_lc in words:
                    words[word_lc] += 1
                else:
                    words[word_lc] = 1

            # Increment total word count
            wordcount += len(words_now)

        # No valid ASCII text found in the file
        if not found_text:
            resp = {
                'error': 'File does not contain valid ASCII text, possibly corrupted or not a text file.'
            }
            return Response(resp, 400)

        return {
            'wordcount': wordcount,
            'words': words,
            'lines': line_nr,
            'error_lines': error_lines
        }

    def put(self, request, format=None):
        """
        Handles processing uploaded file and saving information to database.
        """
        data = self.process_file(request.data['file'])

        # Save results to DB
        File = FileUpload(
            wordcount=data['wordcount'],
            words=data['words'],
            lines=data['lines']
        )
        File.save()

        # Create response object
        resp = {
            'wordcount': data['wordcount'],
            'words': data['words'],
            'lines': data['lines'],
        }

        # Lines with errors were encountered
        if data['error_lines']:
            resp['error'] = '%d lines could not be parsed as valid ASCII and have been skipped.' % len(data['error_lines'])

        return Response(resp, 200)
