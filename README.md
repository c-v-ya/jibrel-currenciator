# Currenciator

Django app for getting currency rates from [bitfinex](bitfinex.com).

Tested with python 3.7, should work with v.3+.

## Dependencies

See `requirements.txt`.

## Running

Before starting specify and adjust `env` variables as below:

    DEBUG=True
    SITE_IP=*

Optionally specify DB connection values:

    DB_NAME
    DB_USER
    DB_PASSWORD
    DB_HOST
    DB_PORT

or create DB with the same name, user and password as in `settings.py`.

Don't forget to create application user via

    python manage.py createsuperuser

Load fixtures

    python manage.py loaddata currencies

Optionally run management command to populate rates in database

    python manage.py updaterates

When running on linux systems, you can set above command to run every 5 hours

    python manage.py crontab add
    
Note that it requires `cron/cronie` to be installed in the system.
