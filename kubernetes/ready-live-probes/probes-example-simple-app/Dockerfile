FROM python:3.9-slim-buster

WORKDIR /app

RUN apt update -y && apt install -y curl

COPY requirements.txt requirements.txt

RUN pip install -r ./requirements.txt

COPY . /app

COPY . /action.sh
RUN chmod 777 action.sh

CMD [ "python3", "app.py"]
