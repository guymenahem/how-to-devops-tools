FROM python:3.9-slim-buster

WORKDIR /app-no-probes

COPY requirements.txt requirements.txt

RUN pip install -r ./requirements.txt

COPY . /app-no-probes

CMD [ "python3", "app-no-probes.py"]
