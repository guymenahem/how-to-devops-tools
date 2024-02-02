FROM python:3.9

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY generated_code/ generated_code/

COPY server.py ./

EXPOSE 8080

# Run the gRPC server script when the container launches
CMD ["python", "server.py"]
