#!/usr/bin/env python

import asyncio

import pyaudio
from websockets.asyncio.server import serve

from main import SpeechParser


async def handler(websocket):
    # Initialize voice recognition
    mic = pyaudio.PyAudio()
    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True)
    stream.start_stream()

    speech_parser = SpeechParser(
        model_path="speech_to_resonite/data/models/vosk-model-small-en-us-0.15",
        database_path="speech_to_resonite/data/dictionaries/resonite-node-database.json",
        custom_words_path="speech_to_resonite/data/dictionaries/custom-words.json",
    )

    speech_parser.start_listening()

    # Save the last message, and only send a new message when it is different
    last_message = None

    while True:
        if speech_parser.result != last_message:
            last_message = speech_parser.result

            # Important, some of this needs to have an await keyword, or it generates cryptic errors
            await websocket.send(last_message)

        await asyncio.sleep(1)


async def main():
    async with serve(handler, "", 8001):
        await asyncio.get_running_loop().create_future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
