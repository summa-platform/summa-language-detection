FROM ubuntu:16.04

RUN apt-get update && apt-get install -y python3-pip && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip

# Install RabbitMQ client and the language detection library
RUN pip3 install aio-pika==0.21.0 langdetect==1.0.7

WORKDIR /opt/app

ADD . /opt/app

ENV LANG C.UTF-8
ENV PYTHONUNBUFFERED y

ENTRYPOINT ["/opt/app/rabbitmq.py"]
