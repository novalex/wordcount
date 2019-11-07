"""
Define tests.
"""

import random
from django import urls
from rest_framework.test import APIClient, APITestCase
from wordcount.settings import WORDCOUNT_API


class FileUploadTests(APITestCase):
    """
    Test file upload and parsing functionality.
    """
    def __init__(self, methodName):
        super().__init__(methodName=methodName)
        self.url = urls.reverse('fileupload')
        self.wordcount = random.randint(1, 999)
        self.words = {}

    def _test_content(self):
        """
        Generate random string for testing wordcount.
        """
        test_words = [
            'hello',
            'world',
            'this',
            'is',
            'a',
            'test'
        ]
        string = ''
        i = 1
        while i <= self.wordcount:
            j = random.randint(0, len(test_words) - 1)
            word_now = test_words[j]
            string += ' ' + word_now
            if word_now in self.words:
                self.words[word_now] += 1
            else:
                self.words[word_now] = 1
            i += 1

        return string

    def test_upload_file_success(self):
        """
        Test file upload (POST method) and check the validity of the returned result.
        This test checks success conditions.
        """
        # Assert file can be uploaded
        client = APIClient(HTTP_CONTENT_DISPOSITION='attachment; filename=testfile_success')
        resp = client.post(self.url, self._test_content(), content_type='text/plain')
        self.assertEqual(resp.status_code, 200)

        # Assert that the required information is returned
        for data_key in ['id', 'wordcount', 'words']:
            self.assertIn(data_key, resp.data)

        # Assert that the correct wordcount is returned.
        self.assertEqual(self.wordcount, resp.data['wordcount'])
        self.assertEqual(self.words, resp.data['words'])

    def test_upload_file_too_large(self):
        """
        Test file upload with content larger than the maximum allowed.
        This test checks failure conditions.
        """
        # Assert that an error is returned when content is at least 1 byte over the allowed size
        client = APIClient(HTTP_CONTENT_DISPOSITION='attachment; filename=testfile_failure')
        content = 'x' * (WORDCOUNT_API['MAX_FILESIZE'] + 1)
        resp = client.post(self.url, content, content_type='text/plain')
        self.assertEqual(resp.status_code, 413)

    def test_upload_file_invalid_ascii(self):
        """
        Test file without valid ASCII.
        This test checks failure conditions.
        """
        # Assert that an error is returned when content does not contain valid ASCII
        client = APIClient(HTTP_CONTENT_DISPOSITION='attachment; filename=testfile_failure')
        resp = client.post(self.url, 'ö', content_type='text/plain')
        self.assertEqual(resp.status_code, 400)

    def test_list_all_results(self):
        """
        Test result listing functionality (GET method).
        """
        # Create test results in the DB
        results = 3
        client = APIClient(HTTP_CONTENT_DISPOSITION='attachment; filename=testfile_list')
        i = 1
        while i <= results:
            client.post(self.url, 'test content %d' % i, content_type='text/plain')
            i += 1

        # List all results
        client = APIClient()
        resp = client.get(self.url)
        # Assert that the correct number of results is returned
        self.assertEqual(results, len(resp.data))

    def test_list_single_result(self):
        """
        Test single result listing functionality (GET method with id query arg).
        This test checks success and failure conditions.
        """
        # Create test result in DB
        client = APIClient(HTTP_CONTENT_DISPOSITION='attachment; filename=testfile_single_list')
        resp = client.post(self.url, 'test content', content_type='text/plain')
        # Check listing of returned result id
        resp = client.get(self.url + '?id=%d' % resp.data['id'])
        self.assertEqual(resp.status_code, 200)
        # Check listing non-existing result id
        resp = client.get(self.url + '?id=999')
        self.assertEqual(resp.status_code, 404)
