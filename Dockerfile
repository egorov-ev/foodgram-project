FROM python:3.8.5
LABEL maintainer='EgorovEgor'
WORKDIR /code
COPY . .
RUN apt update && apt install wkhtmltopdf -y
RUN pip install -r /code/requirements.txt
CMD gunicorn grocery_assistant.wsgi:application --bind 0.0.0.0:8000
