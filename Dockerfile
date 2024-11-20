FROM python:3.9-alpine3.13

LABEL maintainer="labete56"

ENV PYTHONUNBUFFERED=1

# Install dependencies and set up virtual environment
COPY ./requirements.txt /temp/requirements.txt
COPY ./requirements.dev.txt /temp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .temp-build-deps \
        build-base postgresql-dev musl-dev 
RUN /py/bin/pip install -r /temp/requirements.txt && \
    if [ "$DEV" = "true" ]; then /py/bin/pip install -r /temp/requirements.dev.txt; fi && \
    rm -rf /temp && \
    apk del .temp-build-deps

RUN adduser --disabled-password --no-create-home django-user

ENV PATH="/py/bin:$PATH"

USER django-user

# Optionally add CMD to run the app, for example:
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
