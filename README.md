# Python Wordcount REST  API

RESTful wordcount API using Python and the [Django REST Framework](https://www.django-rest-framework.org/).

## What the API does:
- Accepts text (ASCII) file uploads (up to 10MB).
- Returns the total wordcount and number of occurences for each word in the uploaded file.
- Saves results to DB.
- Allows querying all results or individual result by ID.
- Allows skipping words containing a specific character or string.
- Allows spell-checking the content against the Bing Spell Check API.

### To start service
Execute `docker-compose up` from the root dir. The web service will become available at `0.0.0.0:8000`.

Execute `docker-compose exec web python manage.py migrate` to create the database tables.

### To use API
**Uploading**: do a `POST` request to `0.0.0.0:8000` with the raw file data as body and a `Content-Disposition: attachment; filename=testfile` header;
- You should receive a 200 response code with JSON data containing the wordcount, line count and list of individual words and their count.
- If no file is uploaded, a 400 code will be reurned with a relevant message.
- If file is larger than 10MB, a 413 code will be returned with a relevant message.
- If file does not contain any lines with valid ASCII, a 400 code will be returned with a relevant message.
- If the 'skip_words_containing' query arg is set (e.g. `0.0.0.0:8000?skip_words_containing=blue`), all words containing the specified value (e.g. "blue") within them will be removed from the result and not be counted.
- If the 'check_spelling' query arg is set (e.g. `0.0.0.0:8000?check_spelling`), the words found in the file will be spell-checked and any misspelled words will be returned in the response under "words.misspelled_words".
  - Make sure your API key is set under `SPELLCHECK_API_KEY` in the settings file.
  - Capitalization mistakes will not be included in the result, e.g. for proper nouns.

**Listing all results**: do a `GET` request to `0.0.0.0:8000` or visit the address in a browser;
- You should get a 200 response code with JSON data containing the ID, wordcount and line count for each result.
- If no results exist in the DB, an empty array will be returned.

**Listing single result**: do a `GET` request to `0.0.0.0:8000?id={{id}}` or visit the address in a browser;
- You should get a 200 response code with JSON data containing the ID, wordcount, line count and list of individual words and their count for the result with the specified ID.
- If a result with the specified ID does not exist, a 404 code will be returned along with a relevant message.

Grab the Postman request collection [here](https://www.getpostman.com/collections/46a2d3a9ead5d9a1f486).

### To run tests
Execute `docker-compose exec web python manage.py test`.

### Mentions
- The file size limit uses decimal bytes, i.e. `10MB = 10,000,000B`.
- Parser removes undesirable characters before splitting the words, but it is far from perfect and things like breaking hyphens will not work properly.
- All words in the response will be lowercased in order to show the total count for each word occurence, regardless of the original case.

### Resources
- [Docker compose setup](https://docs.docker.com/compose/django/) with Django and PostgresSQL
- Debugging setup with [ptvsd](https://github.com/Microsoft/ptvsd) and help from [this guide](https://gist.github.com/veuncent/1e7fcfe891883dfc52516443a008cfcb)