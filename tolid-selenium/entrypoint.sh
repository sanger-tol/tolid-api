#!/bin/sh
# SPDX-FileCopyrightText: 2021 Genome Research Ltd.
#
# SPDX-License-Identifier: MIT

envsubst < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf && \
cat /etc/nginx/nginx.conf && \
nginx -g "daemon off;" & \

sleep 10s && \
/opt/bin/entry_point.sh
