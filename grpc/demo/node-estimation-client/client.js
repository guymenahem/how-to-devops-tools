const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');

const PROTO_PATH = 'buying_intent.proto';
const targetServer = process.env.TARGET_SERVER || 'localhost';
console.log('target server is ' + targetServer)


const packageDefinition = protoLoader.loadSync(PROTO_PATH, {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true,
});

const buyingIntentProto = grpc.loadPackageDefinition(packageDefinition).buying_intent;

const client = new buyingIntentProto.BuyingIntentService(targetServer + ':8080', grpc.credentials.createInsecure());

function makeGrpcRequest() {
    const request = {
        userName: 'John',
        productName: 'Item',
        price: 50.0,
        lastActivityTimestamp: Date.now(),
    };

    client.GetBuyingIntent(request, (error, response) => {
        if (!error) {
            console.log(`Received response: ${JSON.stringify(response)}`);
        } else {
            console.error(`Error: ${error.message}`);
        }
    });
}

// Make a gRPC request every 2 seconds
setInterval(makeGrpcRequest, 2000);
