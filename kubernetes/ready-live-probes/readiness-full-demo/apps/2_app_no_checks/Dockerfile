FROM python:3.9-slim-buster

WORKDIR /app-no-checks

COPY requirements.txt requirements.txt

RUN pip install -r ./requirements.txt

COPY . /app-no-checks

CMD [ "python3", "app-no-checks.py"]
