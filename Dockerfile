FROM python:3.8.5

LABEL author="andyi95"
LABEL release-date="2021-09-06"

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && pip install -r /app/requirements.txt

COPY . /app

CMD python manage.py makemigrations && python manage.py migrate && gunicorn battleship_django_ws.asgi:application -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:80