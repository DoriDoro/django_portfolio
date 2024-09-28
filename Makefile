data:
	python manage.py create_data

shell:
	python manage.py shell

create_db:
	python manage.py makemigrations
	python manage.py migrate

server:
	python manage.py runserver

g_server:
	gunicorn portfolio.wsgi:application

makemessages:
	python manage.py makemessages --all

compilemessages:
	PYTHONPATH=/home/doro/Desktop/django_portfolio python manage.py compilemessages
