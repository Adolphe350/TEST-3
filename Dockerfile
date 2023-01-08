# syntax=docker/dockerfile:1
FROM python:3


COPY requirements.txt ./
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . /yalaweb
WORKDIR /yalaweb

ENTRYPOINT ["./gunicorn.sh"]