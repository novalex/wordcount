# Python Wordcount REST  API

RESTful wordcount API using Python and the [Django REST Framework](https://www.django-rest-framework.org/).

## What the API does:
- Accepts text (ASCII) file uploads (up to 10MB);
- Returns the total wordcount and number of occurences for each word in the uploaded file;

### To start service
Execute `docker-compose up` from the root dir. The web service will become available at `0.0.0.0:8000`.
Execute `docker-compose exec web python manage.py migrate` to create the database tables.

### Resources
- [Docker compose setup](https://docs.docker.com/compose/django/) with Django and PostgresSQL