FROM python:3.11-slim

WORKDIR /app

RUN pip install gunicorn

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY link_shortener/ .

CMD [ "gunicorn", "--bind", "0.0.0.0:8000", "link_shortener.wsgi:application" ]