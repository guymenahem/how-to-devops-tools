FROM python:3.9-slim-buster

WORKDIR /app

RUN apt update -y && apt install -y curl && apt-get -y install libpq-dev gcc

COPY requirements.txt requirements.txt

RUN pip install -r ./requirements.txt

COPY . /app

COPY . /action.sh

CMD [ "python3", "app-adv-check.py"]
