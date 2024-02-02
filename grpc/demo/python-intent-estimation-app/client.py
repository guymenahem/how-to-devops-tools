import grpc
import time
import random
from generated_code import buying_intent_pb2
from generated_code import buying_intent_pb2_grpc

def generate_random_user_info():
    return buying_intent_pb2.UserBuyingInfo(
        userName=f"User_{random.randint(1, 100)}",
        productName=f"Product_{random.randint(1, 100)}",
        price=random.uniform(10.0, 100.0),
        lastActivityTimestamp=int(time.time())
    )

def make_grpc_request(stub):
    request = generate_random_user_info()

    try:
        response = stub.GetBuyingIntent(request)
        print(f"Response: {response.buyingIntentScore}")
    except grpc._channel._InactiveRpcError:
        print("RPC error")

def main():
    channel = grpc.insecure_channel('localhost:8080')
    stub = buying_intent_pb2_grpc.BuyingIntentServiceStub(channel)

    try:
        while True:
            make_grpc_request(stub)
            time.sleep(2)
    except KeyboardInterrupt:
        print("Client stopped by user.")

if __name__ == '__main__':
    main()
