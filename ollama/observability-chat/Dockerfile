FROM python:3.11-slim-buster

WORKDIR /app

RUN apt update -y && apt install -y curl

COPY requirements.txt requirements.txt

RUN pip install -r ./requirements.txt

COPY . /app

CMD [ "python3", "app.py"]
