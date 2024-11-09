import asyncio

from websockets.asyncio.server import serve


class WebsocketServer:
    def __init__(self, message_queue, stop_event, host="127.0.0.1", port=8069):
        self.message_queue = message_queue
        self.stop_event = stop_event
        self.host = host
        self.port = port
        self.connections = set()

    async def handler(self, websocket):
        print("Connection established")
        self.connections.add(websocket)
        try:
            while not self.stop_event.is_set():
                message = await self.message_queue.get()
                speech, parsed = message

                send_tasks = [
                    websocket.send(f"SPK-{speech}CMD-{parsed}")
                    for websocket in self.connections
                ]
                asyncio.gather(*send_tasks)
                print(f">>>Speech: {speech}")
                print(f">>>Parsed: {parsed}")

        finally:
            self.connections.remove(websocket)

    async def start(self):
        print("Starting websocket")

        async with serve(self.handler, self.host, self.port):
            print(f"WebSocket server started at ws://{self.host}:{self.port}")
            # Keep the server running until stop_event is set
            await self.stop_event.wait()
