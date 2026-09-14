# SPDX-FileCopyrightText: 2024 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

FROM gitlab-registry.internal.sanger.ac.uk/tol/tol-core/api-base:2.0.1

ENV PYTHONDONTWRITEBYTECODE = 1
ENV UWSGI_CHEAPER = 4
ENV UWSGI_PROCESSES = 64

COPY app/requirements.txt /app

RUN pip3 --no-cache-dir install -r requirements.txt

COPY ./app /app
COPY ./migrations /migrations
