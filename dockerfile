FROM python:3.6
ENV LANG en_US.utf8
WORKDIR /code
ADD requirements.txt /code
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get install -y default-mysql-client
