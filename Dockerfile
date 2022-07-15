FROM nvidia/cuda:11.4.1-cudnn8-devel-ubuntu20.04 AS base

RUN apt-get -y update
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get install -y python3.9 python3-pip
COPY requirements.txt /requirements/
RUN pip install -r requirements/requirements.txt --no-cache-dir

EXPOSE 5000

RUN mkdir /app
COPY app.py /app
COPY imagenet_class_index.json /app
WORKDIR /app

ENTRYPOINT ["python3"]
CMD ["app.py"]
