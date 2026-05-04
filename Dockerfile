FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./pyproject.toml .
COPY ./README.md .
RUN pip install --upgrade pip && pip install --no-cache-dir .

COPY . .

RUN adduser --disabled-password appuser
RUN mkdir -p /app/core/staticfiles && chown -R appuser:appuser /app/core/staticfiles
RUN chmod +x entrypoint.sh

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/')" || exit 1

ENTRYPOINT ["./entrypoint.sh"]