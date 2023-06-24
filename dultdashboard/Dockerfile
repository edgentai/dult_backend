# Fetching official base image for python
FROM python:3.9-slim
# Preventing python from writing
# pyc to docker container
ENV PYTHONDONTWRITEBYTECODE 1
# Flushing out python buffer
ENV PYTHONUNBUFFERED 1
# Updating the os
RUN apt-get -y update && apt-get -y install gcc \
        libssl-dev \
        python3-pip \
        && pip3 install --no-cache-dir pip==23.0.1

# Copying requirement file
COPY ./requirements.txt /requirements.txt
# Installing dependencies
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /home/app/
EXPOSE 8000
# Copying all the files in our project
COPY . .