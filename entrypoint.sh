python manage.py migrate --noinput
exec gunicorn portfolio.wsgi:application --bind 0.0.0.0:8000
