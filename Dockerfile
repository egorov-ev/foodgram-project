FROM python:3.8.5
LABEL maintainer='EgorovEgor'
WORKDIR /code
COPY . .
RUN pip install -r /code/requirements.txt
RUN python3 manage.py collectstatic --noinput
CMD gunicorn grocery_assistant.wsgi:application --bind 0.0.0.0:8000