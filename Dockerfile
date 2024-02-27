# pull official base image
FROM python:3.11-bullseye

LABEL maintainer="Adeleke Oluwafemi"

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 

# install necessary packages
RUN apt-get update && \
    apt-get -y install gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# set the working directory
WORKDIR /app

# copy the source code
COPY . /app/

RUN apt-get update && apt-get install -y netcat


# install pip project dependencies
RUN pip install --upgrade pip && \
    pip install --trusted-host pypi.python.org -r requirements.txt


# expose ports
EXPOSE 8000


# Use the gunicorn_config.py as the Gunicorn configuration file
CMD ["gunicorn", "-c", "gunicorn_config.py", "config.wsgi:application"]
