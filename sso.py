import asyncio
import websockets
import logging
import json
import ssl

logging.basicConfig(level = logging.INFO)

async def consumer_handler(websocket: websockets.WebSocketClientProtocol()):
    msg = json.dumps({"command": "subscribe", "channel": "1003"})
    async for message in websocket:
        # await websocket.send(msg)
        log_message(message)


async def consume(hostname: str):
    websocket_resource_url = f"wss://{hostname}"
    async with websockets.connect(websocket_resource_url) as websocket:
        # websocket.send("\"command\": \"subscribe\", \"channel\": 1003")
        await consumer_handler(websocket)

def log_message(message: str):
    d = json.loads(message)
    # if len(d) == 3:
    #     print(d[2][0],':',d[2][1],':',d[2][2])
    print(d['data'])

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # loop.run_until_complete(consume(hostname="api2.poloniex.com"))
    loop.run_until_complete(consume('stream.binance.com:9443/stream?streams=ethbtc@aggTrade'))
    loop.run_forever()



# ws.send(json.dumps([json.dumps({'msg': 'connect', 'version': '1', 'support': ['1', 'pre2', 'pre1']})])) result = ws.recv()