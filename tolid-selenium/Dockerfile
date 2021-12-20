FROM selenium/standalone-chrome

USER root

RUN sudo apt-get update && apt-get upgrade -y

RUN sudo apt-get install -y gettext-base nginx bash

COPY nginx.conf.template /etc/nginx/

COPY entrypoint.sh /bin/setup-entrypoint.sh

ENTRYPOINT [ "/bin/setup-entrypoint.sh" ]
