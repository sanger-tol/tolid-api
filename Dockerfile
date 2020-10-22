FROM alpine:3.10
FROM python:buster
FROM gcc:latest

# Dockerize is needed to sync containers startup
ENV DOCKERIZE_VERSION v0.6.0
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-alpine-linux-amd64-$DOCKERIZE_VERSION.tar.gz

RUN mkdir -p /usr/src/app/instance
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
COPY setup.py /usr/src/app/
COPY start.sh /usr/src/app/
COPY config.json /usr/src/app/

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-setuptools
RUN pip3 install --upgrade setuptools
RUN python3 setup.py install
RUN pip3 --no-cache-dir install -r requirements.txt
RUN pip3 --no-cache-dir install 'connexion[swagger-ui]' 

#RUN curl -s https://gitlab.com/wtsi-grit/darwin-tree-of-life-sample-naming/-/raw/master/final_merged.txt -o final_merged.txt
#RUN curl -s https://gitlab.com/wtsi-grit/darwin-tree-of-life-sample-naming/-/raw/master/unique_ids_assigned.txt -o unique_ids_assigned.txt

# Copy the test config file into the local instance if it does not exist
RUN cp -n config.json /usr/src/app/instance/config.json 
RUN cat /usr/src/app/instance/config.json 

#RUN chmod +x start.sh
COPY . /usr/src/app

EXPOSE 8080
CMD ["python3", "-m", "swagger_server"]
# RUN ./start.sh