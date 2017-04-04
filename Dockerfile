FROM ubuntu
RUN apt-get update && apt-get upgrade
RUN apt-get -y install ansible
RUN pip install wiper

COPY . /opt

WORKDIR /opt/acibootstrap
