from vosk import Model, KaldiRecognizer
import json
import pyaudio
import sys
import os
import threading

from phonetic_fuzz_search import PhoneticFuzzSearch

DEBUG = True


def list_difference(list1, list2):
    return [x for x in list1 if x not in list2]


class SpeechParser:
    def __init__(
        self,
        model_path=None,
        database_path=None,
        custom_words_path=None,
    ):
        if not os.path.exists(model_path):
            print(
                "Please download a model from https://alphacephei.com/vosk/models and unpack it to speech_to_resonite/models/"
            )
            sys.exit(1)

        self.debug = DEBUG
        self.listening = False
        self.result = None

        self.database_path = database_path
        self.custom_words_path = custom_words_path

        self.model_path = model_path
        self.get_model()

        self.get_database()
        self.recognizer.SetWords(True)
        self.recognizer.SetGrammar(grammar=self.dictionary)

        self.get_finder()
        self.finder.debug = self.debug

    def debugging_print(self, *args, **kwargs):
        if self.debug:
            print(*args, **kwargs)

    def get_finder(self):
        if not self.database_path or not os.path.exists(self.database_path):
            print(
                f"Error: could not find the dictionary. Database path = {self.database_path}"
            )
            sys.exit(1)
        self.finder = PhoneticFuzzSearch(self.database_path)

    def get_model(self):
        print(self.model_path)
        self.model = Model(self.model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)

    def get_database(self):
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

    def parse_speech(self, speech: str):
        self.debugging_print("Parsing:", speech)

        speech = self.swap_bindings(speech)
        speech = speech.replace(" ", "")

        self.debugging_print("Sending:", speech)

        node = self.finder.search_node(speech)
        self.debugging_print("Found:", node)

        return node

    def listen_loop(self):
        """
        Internal function to continuously listen for audio inputs and parse them.
        """
        while self.listening:
            data = stream.read(4096)

            if self.recognizer.AcceptWaveform(data):
                result = self.recognizer.Result()
                result = json.loads(result)
                text = result["text"]

                if text == "":
                    continue

                node = self.parse_speech(text)
                self.result = node
                print(self.result)

    def start_listening(self):
        """
        Begins to listens Read SpeechParser.result to read the result.
        """
        if not self.listening:
            self.listening = True
            self.listen_thread = threading.Thread(
                target=self.listen_loop, name="VoskParsesListening"
            )
            self.listen_thread.start()

    def stop_listening(self):
        """
        Stops the listening thread
        """
        self.listening = False
        if self.listen_thread is not None:
            self.listen_thread.join()
            self.listen_thread = None


if __name__ == "__main__":
    speech_parsesr = SpeechParser(
        model_path="speech_to_resonite/data/models/vosk-model-small-en-us-0.15",
        database_path="speech_to_resonite/data/dictionaries/resonite-node-database.json",
        custom_words_path="speech_to_resonite/data/dictionaries/custom-words.json",
    )
    mic = pyaudio.PyAudio()

    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True)
    stream.start_stream()

    speech_parsesr.start_listening()
