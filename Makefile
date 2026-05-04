secret_key:
	python manage.py shell -c 'from django.core.management import utils; print(utils.get_random_secret_key())'

data:
	python manage.py data_create

shell:
	python manage.py shell

create_db:
	python manage.py makemigrations
	python manage.py migrate

server:
	python manage.py runserver

server_5:
	python manage.py runserver 8005

g_server:
	gunicorn portfolio.wsgi:application

makemessages:
	python manage.py makemessages --all

compilemessages:
	PYTHONPATH=/home/doro/Desktop/django_portfolio python manage.py compilemessages
