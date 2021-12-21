# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

FROM python:3.8

RUN apt-get update && apt-get upgrade -y

WORKDIR /src

COPY requirements.txt .

RUN pip3.8 install -r requirements.txt

COPY robot/ .
