FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8000

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "portfolio.wsgi:application", "--bind", "0.0.0.0:8000"]