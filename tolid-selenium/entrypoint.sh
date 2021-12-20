#!/bin/sh

envsubst < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf && \
cat /etc/nginx/nginx.conf && \
nginx -g "daemon off;" & \

sleep 10s && \
/opt/bin/entry_point.sh
