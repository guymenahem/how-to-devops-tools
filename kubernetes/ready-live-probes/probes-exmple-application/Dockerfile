FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r ./requirements.txt

COPY . /app

COPY . /liveness.pid

COPY . /readiness.pid

COPY . /stop-ready
RUN chmod 777 stop-ready

COPY . /stop-live
RUN chmod 777 stop-live

CMD [ "python3", "app.py"]
