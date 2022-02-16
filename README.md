# STAR WARS

Application which allows to derive data from `swapi.dev` API

## Start

To start the application you need to have `docker-compose`, `npm` and `nodejs`.

1. Go to `/frontend`
2. Install npm packages: `npm install`
3. Go to main dir and run:
```bash
docker-compose up --build
```

**Above steps should be done only once.
If you have done it before you can start the application using below command:
```bash
docker-compose up
```

Application is running on below URL:
```bash
http://127.0.0.1:3000
```

To stop the application run:
```bash
docker-compose down
```

## Comments

1. More tests should be added (also in frontend).
2. In a real life scenario all the vulnerable variables like passwords etc. should be stored in a separated file
   (e.g. `.env` file) or set as environment variables and derive straight from there, for example:
```bash
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': os.getenv('db_host'),
        'NAME': os.getenv('db_name'),
        'PASSWORD': os.getenv('db_password'),
        'USER': os.getenv('db_user'),
    }
```
3. No linters/code-checkers-tools have been implemented. Normally project should contain some, for example:
- flake8 and black (backend)
- eslint (frontend)
- pre-commit
4. In a real life scenario I would use also a reverse-proxy like nginx which would serve static files and proxies
requests to an application server.
5. Permissions should be also considered, for example:
- user A: can LIST collections and trigger FETCH a new collection from `swapi.dev` API
- user B: can only LIST collections but cannot FETCH a new collection

## Problems

1. `django-cors-headers` package is installed and set up in the `settings.py` but if any problems with CORS occur
   installing CORS extension in the browser might help.

15-02-2022
