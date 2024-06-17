# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

FROM tiangolo/uwsgi-nginx-flask:python3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV UWSGI_CHEAPER 4
ENV UWSGI_PROCESSES 64

COPY app/requirements.txt /app

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y python3-pip

RUN pip3 --no-cache-dir install -r requirements.txt

COPY ./app /app
COPY ./migrations /migrations
