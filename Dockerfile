FROM ubuntu:18.04

ENV FLASK_CONFIG production
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LANGUAGE en_US:en

RUN apt update && apt upgrade -y
RUN apt install -y poppler-utils python3-pip
RUN apt install -y openjdk-8-jdk
RUN apt install locales -y
RUN apt install -y supervisor
RUN locale-gen --purge && locale-gen en_US.UTF-8


RUN mkdir master
WORKDIR /home/master

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY app app
COPY manage.py general_config.py logger_config.py logger_tools.py boot_flask_service.sh boot_celery_service.sh ./

RUN mkdir logs

EXPOSE 5000
RUN chmod +x boot_flask_service.sh
RUN chmod +x boot_celery_service.sh
ENTRYPOINT ["/usr/bin/supervisord"]
