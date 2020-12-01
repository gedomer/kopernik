FROM python:3.8-slim
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install -r requirements/dev.txt
EXPOSE 8000
