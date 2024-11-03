from vosk import Model, KaldiRecognizer
import json
import asyncio
import sys
import os

from src.phonetic_fuzz_search import PhoneticFuzzSearch


DEBUG = False


def list_difference(list1, list2):
    return [x for x in list1 if x not in list2]


class VoiceHandler:
    def __init__(
        self,
        message_queue,
        stop_event,
        model_path,
        database_path,
        custom_words_path,
        stream=None,
    ):
        if not os.path.exists(model_path):
            print(
                "Please download a model from https://alphacephei.com/vosk/models and unpack it to speech_to_resonite/data/models/"
            )
            sys.exit(1)
        if not message_queue:
            print("Please provide a message queue. asyncio.Queue()")

        self.message_queue = message_queue
        self.stop_event = stop_event

        self.debug = DEBUG
        self.listening = False
        self.result = None

        self.database_path = database_path
        self.custom_words_path = custom_words_path

        self.model_path = model_path
        self._get_model()
        self._get_database()
        self.recognizer.SetWords(True)
        self.recognizer.SetGrammar(grammar=self.dictionary)

        self._get_finder()
        self.finder.debug = self.debug

        self.stream = stream

    def debugging_print(self, *args, **kwargs):
        if self.debug:
            print(*args, **kwargs)

    def _get_finder(self):
        if not self.database_path or not os.path.exists(self.database_path):
            print(
                f"Error: could not find the dictionary. Database path = {self.database_path}"
            )
            sys.exit(1)
        self.finder = PhoneticFuzzSearch(self.database_path)

    def _get_model(self):
        print(self.model_path)
        self.model = Model(self.model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)

    def _get_database(self):
        dictionary = ""

        with open(self.custom_words_path, "r") as f:
            custom_dictionary = json.load(f)

        with open(self.database_path, "r") as f:
            resonite_dictionary = json.load(f)

        # Bindings
        self.bindings = custom_dictionary["bindings"]

        # Grammar
        self.dictionary = resonite_dictionary["grammar"] + custom_dictionary["add"]
        self.dictionary = list_difference(self.dictionary, custom_dictionary["remove"])

        self.dictionary = json.dumps(self.dictionary)

    def swap_bindings(self, text: str):
        for binding in self.bindings:
            text = text.replace(binding["value"], binding["binding"])

        return text

    def search_node(self, speech: str):
        speech = self.swap_bindings(speech)
        query = self.finder.speech_sanitize(speech)

        return self.finder.search_node_exact_caverphone(query)

    def parse_speech(self, speech: str):
        node = self.search_node(speech)
        node = node[0] if node else ""

        return node

    async def listen_loop(self):
        print("Start listening")

        async def read_stream():
            loop = asyncio.get_event_loop()

            while not self.stop_event.is_set():
                # Run the blocking read in a thread pool
                data = await loop.run_in_executor(None, self.stream.read, 4096)
                if self.recognizer.AcceptWaveform(data):
                    result = self.recognizer.Result()
                    result = json.loads(result)

                    speech = result["text"]
                    if speech == "":
                        continue

                    parsed = self.parse_speech(speech)

                    await self.message_queue.put((speech, parsed))

        await read_stream()
