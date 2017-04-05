FROM python:2
RUN apt-get -y update && apt-get -y upgrade
RUN apt-get -y install ansible
RUN apt-get -y install vim

COPY . /opt/acibootstrap

WORKDIR /opt/acibootstrap

RUN pip install -r requirements.txt

CMD acibootstrap.sh