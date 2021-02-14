FROM python:3.8.5
LABEL maintainer='EgorovEgor'
WORKDIR /code
COPY . .
#RUN pip install -r /code/requirements.txt
RUN set -ex \
&& apk add --update --upgrade --no-cache --virtual .build-deps \
cairo-dev pango-dev gdk-pixbuf cairo ttf-freefont ttf-font-awesome \
musl-dev gcc postgresql-dev jpeg-dev zlib-dev libffi-dev \
&& pip install -r requirements.txt \
&& python3 manage.py collectstatic --noinput
CMD gunicorn grocery_assistant.wsgi:application --bind 0.0.0.0:8000