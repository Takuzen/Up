FROM python:3.7.2
ENV LANG en_US.utf8
WORKDIR /code
ADD requirements.txt /code
RUN pip install -r requirements.txt
