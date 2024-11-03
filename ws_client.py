import asyncio
import sys

from websockets.asyncio.client import connect


async def hello():

    uri = "ws://127.0.0.1:8069"

    try:
        async with connect(uri) as websocket:
            print("Connection established")
            while True:
                message = await websocket.recv()
                print(message)

    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":

    asyncio.run(hello())
