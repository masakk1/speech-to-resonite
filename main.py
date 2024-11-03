from src.voice_handler import VoiceHandler
from src.websocket_server import WebsocketServer
import asyncio
import pyaudio


async def main():
    message_queue = asyncio.Queue()
    stop_event = asyncio.Event()

    voice_handler = VoiceHandler(
        message_queue=message_queue,
        stop_event=stop_event,
        model_path="data/models/vosk-model-small-en-us-0.15",
        database_path="data/dictionaries/resonite-node-database.json",
        config_path="data/config.json",
    )
    ws = WebsocketServer(message_queue, stop_event, "127.0.0.1", 8069)

    mic = pyaudio.PyAudio()
    stream = mic.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=4096,
    )
    voice_handler.stream = stream

    print("\n\n\n\n\n\n\nstaring tasks")

    try:
        await asyncio.gather(
            ws.start(),
            voice_handler.listen_loop(),
        )
    finally:
        stream.stop_stream()
        stream.close()
        mic.terminate()
        stop_event.set()


if __name__ == "__main__":
    asyncio.run(main())
