FROM python:3.8
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /code
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
COPY locale.gen /etc/
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y locales

RUN dpkg-reconfigure --frontend=noninteractive locales && \
    update-locale LANG=en_US.UTF-8

RUN mkdir /code
WORKDIR /code
COPY ./requirements.txt /code/
RUN pip install -r requirements.txt
