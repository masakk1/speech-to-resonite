import json
import abydos.phonetic
from rapidfuzz import process
import metaphone
import phonetics
from num2words import num2words
import re
import Levenshtein as lev
import abydos


def remove_list_dulicates(ls: list) -> list:
    return list(set(ls))


def convert_numbers_to_words(input_string):
    def replace_number(match):
        number = match.group(0)  # Get the matched number
        return num2words(number)  # Convert to words

    return re.sub(r"\d+", replace_number, input_string)


class PhoneticFuzzSearch:

    def __init__(self, database_path="dictionaries/resonite-node-database.json"):
        self.debug = False

        self.database_path = database_path
        self._get_database()
        self._get_encoders()

    def debugging_print(self, *args, **kwargs):
        if self.debug:
            print(*args, **kwargs)

    def _get_database(self):
        with open(self.database_path, "r") as f:
            self.database = json.load(f)

        self.nodes = self.database["nodes"]

    def _get_encoders(self):
        self.node_encoders = {
            "soundex": abydos.phonetic.Soundex(),
            "refinedsoundex": abydos.phonetic.RefinedSoundex(),
            "metaphone": abydos.phonetic.Metaphone(),
            "doublemetaphone": abydos.phonetic.DoubleMetaphone(),
            "nysiis": abydos.phonetic.NYSIIS(),
            "caverphone": abydos.phonetic.Caverphone(),
            "daitchmokotoff": abydos.phonetic.DaitchMokotoff(),
            "mra": abydos.phonetic.MRA(),
            "phonex": abydos.phonetic.Phonex(),
            "phonix": abydos.phonetic.Phonix(),
            "beidermorse": abydos.phonetic.BeiderMorse(),
            "fuzzysoundex": abydos.phonetic.FuzzySoundex(),
            "onca": abydos.phonetic.ONCA(),
            "metasoundex": abydos.phonetic.MetaSoundex(),
        }

    def speech_sanitize(self, speech: str):
        speech = speech.lower().replace(" ", "").replace("_", "")
        speech = convert_numbers_to_words(speech)
        return speech

    def _search_fuzzy(self, query: str, list, limit) -> list:
        return process.extract(query, list, limit=limit)

    def _code_metaphone(self, query: str):
        return abydos.phonetic.metaphone(query)

    def _code_double_metaphone(self, query: str):
        return abydos.phonetic.double_metaphone(query)

    def _code_nysiis(self, query: str):
        return abydos.phonetic.nysiis(query)

    def _node_search_exact(self, query: str, node_attribute) -> list:
        matches = []
        for node in self.nodes:
            if query == node[node_attribute]:
                matches.append(node)

        return matches

    def _node_search_fuzzy(self, query: str, node_attribute) -> list:
        matches = process.extract(query, [node[node_attribute] for node in self.nodes])

        matches = remove_list_dulicates(matches)

        for match in matches:
            code, _, _ = match
            for node in self.nodes:
                if node[node_attribute] == code:
                    matches.append(node)

        return matches

    def _matches_select_name_fuzzy(self, query: str, node_matches: list):
        return process.extractOne(
            query, [node["name"].lower() for node in node_matches]
        )

    def _search_template(
        self,
        query: str,
        code_gen_func: callable,
        code_name: str,
        code_search_func: callable,
        match_select_func: callable,
    ) -> list:
        query = self.speech_sanitize(query)

        code = code_gen_func(query)
        matches = code_search_func(code, code_name)
        node_found = match_select_func(query, matches)

        return node_found

    def search_node_exact_metaphone(self, query: str):
        return self._search_template(
            query,
            self.node_encoders["metaphone"].encode,
            "metaphone",
            self._node_search_exact,
            self._matches_select_name_fuzzy,
        )

    def search_node_fuzzy_metaphone(self, query: str):
        return self._search_template(
            query,
            self.node_encoders["metaphone"].encode,
            "metaphone",
            self._node_search_fuzzy,
            self._matches_select_name_fuzzy,
        )

    def search_node_exact_caverphone(self, query: str):
        return self._search_template(
            query,
            self.node_encoders["caverphone"].encode,
            "caverphone",
            self._node_search_exact,
            self._matches_select_name_fuzzy,
        )
