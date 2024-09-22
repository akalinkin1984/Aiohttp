FROM python:3

RUN mkdir /app
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

CMD ["./start.sh"]