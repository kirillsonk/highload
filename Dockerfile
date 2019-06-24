FROM ubuntu:16.04
MAINTAINER Kirill Sonk

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install python3-pip
RUN pip3 install configparser
RUN pip3 install pathlib
RUN pip3 install urllib3

#CMD cd ./server && python ./server/server.py

# Копируем исходный код в Docker-контейнер
ADD ./ $WORK/

EXPOSE 80

WORKDIR $WORK/server

# Запуск
CMD python3 -u ./server.py