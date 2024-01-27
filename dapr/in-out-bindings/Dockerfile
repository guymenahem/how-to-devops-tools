FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r ./requirements.txt

COPY . /app

CMD [ "python3", "app.py"]
