# Python Wordcount REST  API

RESTful wordcount API using Python and the [Django REST Framework](https://www.django-rest-framework.org/).

## What the API does:
- Accepts text (ASCII) file uploads (up to 10MB).
- Returns the total wordcount and number of occurences for each word in the uploaded file.
- Saves results to DB.
- Allows querying all results or individual result by ID.

### To start service
Execute `docker-compose up` from the root dir. The web service will become available at `0.0.0.0:8000`.
Execute `docker-compose exec web python manage.py migrate` to create the database tables.

### To use API
- Uploading: do a `POST` request to `0.0.0.0:8000` with the raw file data as body and a `Content-Disposition: attachment; filename=testfile` header;
  - You should receive a 200 response code with JSON data containing the wordcount, line count and list of individual words and their count.
  - If no file is uploaded, a 400 code will be reurned with a relevant message.
  - If file is larger than 10MB, a 413 code will be returned with a relevant message.
  - If file does not contain any lines with valid ASCII, a 400 code will be returned with a relevant message.
- Listing all results: do a `GET` request to `0.0.0.0:8000` or visit the address in a browser;
  - You should get a 200 response code with JSON data containing the ID, wordcount and line count for each result.
  - If no results exist in the DB, an empty array will be returned.
- Listing single result: do a `GET` request to `0.0.0.0:8000?id={{id}}` or visit the address in a browser;
  - You should get a 200 response code with JSON data containing the ID, wordcount, line count and list of individual words and their count for the result with the specified ID.
  - If a result with the specified ID does not exist, a 404 code will be returned along with a relevant message.

Grab the Postman request collection [here](https://www.getpostman.com/collections/46a2d3a9ead5d9a1f486).

### Resources
- [Docker compose setup](https://docs.docker.com/compose/django/) with Django and PostgresSQL
- Debugging setup with [ptvsd](https://github.com/Microsoft/ptvsd) and help from [this guide](https://gist.github.com/veuncent/1e7fcfe891883dfc52516443a008cfcb)