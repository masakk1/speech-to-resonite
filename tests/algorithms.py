import unittest
import time

import abydos.phonetic
from speech_to_resonite.src.phonetic_fuzz_search import PhoneticFuzzSearch
import json
import abydos

DICT_PATH = "speech_to_resonite/data/dictionaries/resonite-node-database.json"
QUERIES_PATH = "speech_to_resonite/tests/queries.json"

soundex = abydos.phonetic.Soundex()
refinedsoundex = abydos.phonetic.RefinedSoundex()
metaphone = abydos.phonetic.Metaphone()
doublemetaphone = abydos.phonetic.DoubleMetaphone()
nysiis = abydos.phonetic.NYSIIS()
caverphone = abydos.phonetic.Caverphone()
daitchmokotoff = abydos.phonetic.DaitchMokotoff()
mra = abydos.phonetic.MRA()
phonex = abydos.phonetic.Phonex()
phonix = abydos.phonetic.Phonix()
beidermorse = abydos.phonetic.BeiderMorse()
fuzzysoundex = abydos.phonetic.FuzzySoundex()
onca = abydos.phonetic.ONCA()
metasoundex = abydos.phonetic.MetaSoundex()


class TestPhoneticFuzzSearch(unittest.TestCase):
    def setUp(self):
        print("")

        self.finder = PhoneticFuzzSearch(DICT_PATH)
        self._search_limit = 10

        self.database_path = DICT_PATH
        self.queries_path = QUERIES_PATH
        self.queries = []
        self.node_searchers = {}
        self.node_encoders = {}
        self._get_database()
        self._get_all_queries()
        self._get_node_searchers()
        self._get_encoders()

    def _get_database(self):
        with open(self.database_path, "r") as f:
            self.database = json.load(f)

        with open(self.queries_path, "r") as f:
            self.queries = json.load(f)

        self.nodes = self.database["nodes"]

    def _get_encoders(self):
        self.node_encoders = {
            "soundex": abydos.phonetic.Soundex(),
            "refinedsoundex": abydos.phonetic.RefinedSoundex(),
            "metaphone": abydos.phonetic.Metaphone(),
            #    "doublemetaphone": abydos.phonetic.DoubleMetaphone(),
            "nysiis": abydos.phonetic.NYSIIS(),
            "caverphone": abydos.phonetic.Caverphone(),
            #    "daitchmokotoff": abydos.phonetic.DaitchMokotoff(),
            "mra": abydos.phonetic.MRA(),
            "phonex": abydos.phonetic.Phonex(),
            "phonix": abydos.phonetic.Phonix(),
            #    "beidermorse": abydos.phonetic.BeiderMorse(),
            "fuzzysoundex": abydos.phonetic.FuzzySoundex(),
            "onca": abydos.phonetic.ONCA(),
            "metasoundex": abydos.phonetic.MetaSoundex(),
        }

    def _get_node_searchers(self):
        self.node_searchers = {
            "exact": self.finder._node_search_exact,
            "fuzzy": self.finder._node_search_fuzzy,
        }

    def _get_all_queries(self):
        self.queries["all"] = []
        for i in range(len(self.nodes)):
            name = self.nodes[i]["name"]
            spoken_name = self.finder.speech_sanitize(name)
            self.queries["all"].append([spoken_name, name])

    def _test_template(
        self, name, node_searcher_name, queries, node_searcher_func, *args, **kwargs
    ):
        start_time = time.time()

        score = 0
        for query, real in queries:
            node = node_searcher_func(query, *args, **kwargs)
            if node and node[0] == real.lower():
                score += 1

        end_time = time.time()

        print(
            f"{self._testMethodName[5:]:<15}{name:<10}\t{node_searcher_name:<10}\t{end_time - start_time:.2f}\t{score/len(queries):.4f}"
        )

    def _test_suite(self, encoder, code_name):
        for query_list in self.queries:
            for node_search_func in self.node_searchers:
                self._test_template(
                    query_list,
                    node_search_func,
                    self.queries[query_list],
                    self.finder._search_template,
                    encoder.encode,
                    code_name,
                    self.node_searchers[node_search_func],
                    self.finder._matches_select_name_fuzzy,
                )

    def test_soundex(self):
        self._test_suite(self.node_encoders["soundex"], "soundex")

    def test_refinedsoundex(self):
        self._test_suite(self.node_encoders["refinedsoundex"], "refinedsoundex")

    def test_metaphone(self):
        self._test_suite(self.node_encoders["metaphone"], "metaphone")

    def test_nysiis(self):
        self._test_suite(self.node_encoders["nysiis"], "nysiis")

    def test_caverphone(self):
        self._test_suite(self.node_encoders["caverphone"], "caverphone")

    def test_mra(self):
        self._test_suite(self.node_encoders["mra"], "mra")

    def test_phonex(self):
        self._test_suite(self.node_encoders["phonex"], "phonex")

    def test_phonix(self):
        self._test_suite(self.node_encoders["phonix"], "phonix")

    def test_fuzzysoundex(self):
        self._test_suite(self.node_encoders["fuzzysoundex"], "fuzzysoundex")

    def test_onca(self):
        self._test_suite(self.node_encoders["onca"], "onca")

    def test_metasoundex(self):
        self._test_suite(self.node_encoders["metasoundex"], "metasoundex")


#        self.assertGreaterEqual(score, len(self.queries["uncommon"]))


if __name__ == "__main__":
    unittest.main()
