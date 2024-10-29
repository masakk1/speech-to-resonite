from vosk import Model, KaldiRecognizer
import json
import pyaudio
import sys
import os

from phonetic_fuzz_search import PhoneticFuzzSearch


def list_difference(list1, list2):
    return [x for x in list1 if x not in list2]


class SpeechParser:
    def __init__(self, model_path="models/vosk-model-small-en-us-0.15"):
        if not os.path.exists(model_path):
            print(
                f"Please download a model from https://alphacephei.com/vosk/models and unpack it to {model_path}"
            )
            sys.exit(1)

        self.debug = True

        self.get_finder()
        self.finder.debug = self.debug

        self.model_path = Model(model_path)
        self.get_model()

        self.get_grammar()
        self.recognizer.SetWords(True)
        self.recognizer.SetGrammar(grammar=self.grammar)

    def debugging_print(self, *args, **kwargs):
        if self.debug:
            print(*args, **kwargs)

    def get_finder(self):
        self.finder = PhoneticFuzzSearch("dictionaries/resonite-node-database.json")

    def get_model(self):
        self.model = Model("models/vosk-model-small-en-us-0.15")
        self.recognizer = KaldiRecognizer(self.model, 16000)

    def get_grammar(self):
        grammar = ""

        with open("dictionaries/custom-words.json", "r") as f:
            custom_dictionary = json.load(f)

        with open("dictionaries/resonite-node-database.json", "r") as f:
            resonite_dictionary = json.load(f)

        # Bindings
        self.bindings = custom_dictionary["bindings"]

        # Grammar
        self.grammar = resonite_dictionary["grammar"] + custom_dictionary["add"]
        self.grammar = list_difference(self.grammar, custom_dictionary["remove"])

        self.grammar = json.dumps(self.grammar)

        print(self.bindings)

    def swap_bindings(self, text: str):
        for binding in self.bindings:
            text = text.replace(binding["value"], binding["binding"])

        return text

    def parse_speech(self, speech: str):
        self.debugging_print("Parsing:", speech)
        speech = self.swap_bindings(speech)
        self.debugging_print("Swapped:", speech)

        speech = speech.replace(" ", "")

        node = self.finder.search_node(speech)
        self.debugging_print("Found:", node)

        return None

    def begin_loop(self):
        while True:
            data = stream.read(4096)

            if self.recognizer.AcceptWaveform(data):
                result = self.recognizer.Result()
                result = json.loads(result)
                text = result["text"]

                if text == "":
                    continue

                node = self.parse_speech(text)


if __name__ == "__main__":
    speech_parsesr = SpeechParser(model_path="models/vosk-model-small-en-us-0.15")
    mic = pyaudio.PyAudio()

    stream = mic.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True)
    stream.start_stream()

    speech_parsesr.begin_loop()
