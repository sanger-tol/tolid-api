FROM ubuntu:bionic
FROM python:buster
FROM gcc:latest

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
COPY setup.py /usr/src/app/
COPY start.sh /usr/src/app/

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-setuptools
RUN pip3 install --upgrade setuptools
RUN python3 setup.py install
RUN pip3 --no-cache-dir install -r requirements.txt
RUN pip3 --no-cache-dir install 'connexion[swagger-ui]' 

RUN curl -s https://gitlab.com/wtsi-grit/darwin-tree-of-life-sample-naming/-/raw/master/final_merged.txt -o final_merged.txt
RUN curl -s https://gitlab.com/wtsi-grit/darwin-tree-of-life-sample-naming/-/raw/master/unique_ids_assigned.txt -o unique_ids_assigned.txt

#RUN chmod +x start.sh
COPY . /usr/src/app

EXPOSE 8080
ENTRYPOINT ["python3"]
CMD ["-m", "swagger_server"]
# RUN ./start.sh