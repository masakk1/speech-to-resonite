#!/usr/bin/env python

import asyncio

from websockets.asyncio.server import serve


async def handler(websocket, stop_event, message_queue):
    print("handler")
    last_message = None
    while not stop_event.is_set():
        message = await message_queue.get()
        print(message)
        if last_message == message:
            continue

        await websocket.send(last_message)
        await asyncio.sleep(0.5)


async def websocket_start(message_queue, stop_event, host="", port="5569"):
    print("websocket_start")

    async def wrapper(websocket, path):
        await handler(websocket, message_queue, stop_event)

    async with serve(
        wrapper,
        host=host,
        port=port,
    ):
        await asyncio.get_running_loop().create_future()  # run forever
