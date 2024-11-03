from src.voice_handler import VoiceHandler
from src.websocket_server import websocket_start
import asyncio
import pyaudio


async def main():
    message_queue = asyncio.Queue()
    stop_event = asyncio.Event()

    voice_handler = VoiceHandler(
        message_queue=message_queue,
        model_path="data/models/vosk-model-small-en-us-0.15",
        database_path="data/dictionaries/resonite-node-database.json",
        custom_words_path="data/dictionaries/custom-words.json",
    )

    mic = pyaudio.PyAudio()
    stream = mic.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=4096,
    )
    voice_handler.stream = stream

    voice_handler_task = asyncio.create_task(voice_handler.listen_loop(stop_event))
    websocket_task = asyncio.create_task(websocket_start(message_queue, stop_event))

    asyncio.gather(voice_handler_task, websocket_task)


if __name__ == "__main__":
    asyncio.run(main())
