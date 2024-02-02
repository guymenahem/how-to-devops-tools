import grpc
import os
import sys
from concurrent import futures
import time
import random
import logging
from generated_code import buying_intent_pb2
from generated_code import buying_intent_pb2_grpc

logging.basicConfig(level=logging.INFO)

class BuyingIntentService(buying_intent_pb2_grpc.BuyingIntentServiceServicer):
    def GetBuyingIntent(self, request, context):
        logging.info(f"Received request: {request}")
        score = random.randint(1, 10)
        response = buying_intent_pb2.BuyingIntentResponse(buyingIntentScore=random.randint(1, 10))
        logging.info(f"Responding with: {response}")
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    buying_intent_pb2_grpc.add_BuyingIntentServiceServicer_to_server(BuyingIntentService(), server)
    server.add_insecure_port('[::]:8080')
    server.start()
    logging.info("gRPC server is running on :8080")
    try:
        while True:
            None
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
