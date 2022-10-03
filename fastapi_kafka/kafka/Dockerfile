#===============================================
#======  Using Python 3.9 build Imange =========
#===============================================

# pull official base image
FROM python:3.8.14-buster

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip


RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
# RUN apt install python3.7-dev -y

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt


# copy project
COPY ./worker/ /app/