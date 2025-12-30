FROM python:3.10-alpine
ENV PYTHONUNBUFFERED 1

WORKDIR /back
RUN pip install --upgrade pip

COPY requirements.txt /back/
RUN pip install -r requirements.txt

ADD . /back/