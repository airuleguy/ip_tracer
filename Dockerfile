FROM python:3.9.2
EXPOSE 8000
WORKDIR /src

ADD ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ADD ./iptracker .

CMD python manage.py makemigrations

CMD python manage.py migrate

CMD gunicorn iptracker.wsgi:application -b 0.0.0.0:8000 -w 4  --timeout 120 --log-level debug