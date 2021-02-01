#!/bin/sh

envsubst "\$TOLID_API_LOCATION" < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf && cat /etc/nginx/nginx.conf && nginx -g 'daemon off;'
