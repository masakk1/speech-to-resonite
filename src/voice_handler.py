from vosk import Model, KaldiRecognizer
import json
import asyncio
import sys
import os

from src.phonetic_fuzz_search import PhoneticFuzzSearch


DEBUG = False
DEFAULT_NODE_TYPE_FALLBACK = "float"


def list_difference(list1, list2):
    return [x for x in list1 if x not in list2]


class VoiceHandler:
    def __init__(
        self,
        message_queue,
        stop_event,
        model_path,
        database_path,
        config_path,
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
        self.config_path = config_path

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
        with open(self.config_path, "r") as f:
            config = json.load(f)

        with open(self.database_path, "r") as f:
            resonite_dictionary = json.load(f)

        self.config = config

        # Bindings
        self.bindings = config["bindings"]

        # Grammar
        self.dictionary = resonite_dictionary["grammar"] + config["grammar"]["add"]
        self.dictionary = list_difference(self.dictionary, config["grammar"]["remove"])

        self.dictionary = json.dumps(self.dictionary)

    def swap_bindings(self, text: str, bindings: list):
        for binding in bindings:
            if isinstance(binding["replace"], list):
                for replace in binding["replace"]:
                    text = text.replace(replace, binding["new"])
            else:
                text = text.replace(binding["replace"], binding["new"])

        return text

    def search_node(self, speech: str):
        speech = self.swap_bindings(speech, self.bindings["node"])
        query = self.finder.speech_sanitize(speech)

        return self.finder.search_node_exact_caverphone(query)

    def search_type(self, speech: str):
        speech = self.swap_bindings(speech, self.bindings["node_type"])
        query = self.finder.speech_sanitize(speech)

        result = self.finder.search_type_exact_caverphone(query)
        print(result)
        return result

    def parse_task(self, text: str):
        words = text.split()

        task = {}
        current_key = None
        current_value = []

        for word in words:
            if word.isupper():  # Assuming keys are in uppercase
                if current_key:
                    task[current_key] = " ".join(current_value)
                    current_value = []
                current_key = word
            else:
                current_value.append(word)

        if current_key and current_value:
            task[current_key] = " ".join(current_value)
        elif current_key:
            task[current_key] = ""

        return task

    def handle_task(self, task):
        for key, value in task.items():
            if key == "NEWNODE":
                node = self.search_node(value)
                if node:
                    name = node["name"]
                    path = node["path"]
                    # node_type = node["type"]
                    task["NEWNODE"] = f"{path}.{name}"  # {node_type}"

                else:
                    task = {"ERR": "Node not found"}
            if key == "NODETYPE":
                node_type = self.search_type(value) or {"name": "float"}

                name = node_type["name"]
                task["NODETYPE"] = name

        return task

    def dict_to_string(self, task):
        return " ".join(f"{key} {value}" for key, value in task.items())

    def parse_speech(self, speech: str):
        task_text = self.swap_bindings(speech, self.bindings["cmd"])
        task = self.parse_task(task_text)
        task = self.handle_task(task)

        return self.dict_to_string(task)

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
