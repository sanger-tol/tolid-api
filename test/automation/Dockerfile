# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3-pip

WORKDIR /app/src

COPY requirements.txt .

RUN pip3 --no-cache-dir install -r requirements.txt

COPY . .
