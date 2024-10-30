import unittest
import time
from speech_to_resonite.src.phonetic_fuzz_search import PhoneticFuzzSearch
from num2words import num2words
import re
import json

DICT_PATH = "speech_to_resonite/data/dictionaries/resonite-node-database.json"
QUERIES_PATH = "speech_to_resonite/tests/queries.json"


class TestPhoneticFuzzSearch(unittest.TestCase):
    def setUp(self):
        print("")
        print("Test:", self._testMethodName)
        self.finder = PhoneticFuzzSearch(DICT_PATH)
        self._search_limit = 10

        self.database_path = DICT_PATH
        self.queries_path = QUERIES_PATH
        self.queries = []
        self.rangom_queries = []
        self._get_database()
        self._get_random_queries()

    def _search_node(self, query: str, node_searcher_func: callable):
        query = query.lower()
        found_node = None

        node_matches = node_searcher_func(query, self.nodes, self._search_limit)
        if node_matches == []:
            return None

        fuzzy_matches = self.finder.search_fuzzy(
            query, [node["name"].lower() for node in node_matches], limit=20
        )
        found_node = fuzzy_matches[0]

        return found_node

    def convert_numbers_to_words(self, input_string):
        def replace_number(match):
            number = match.group(0)  # Get the matched number
            return num2words(number)  # Convert to words

        output_string = re.sub(r"\d+", replace_number, input_string)

        return output_string

    def _get_database(self):
        with open(self.database_path, "r") as f:
            self.database = json.load(f)

        with open(self.queries_path, "r") as f:
            self.queries = json.load(f)

        self.nodes = self.database["nodes"]

    def _get_random_queries(self):
        self.random_queries = []
        for i in range(len(self.nodes)):
            query = self.nodes[i]["name"]
            query = query.lower()
            query = self.convert_numbers_to_words(query)
            self.random_queries.append((query, query))

    def test_random_exact_metaphone(self):
        start_time = time.time()

        score = 0
        for query, real in self.random_queries:
            node = self._search_node(query, self.finder.search_node_metaphone)
            if node and node[0] == real.lower():
                score += 1

        end_time = time.time()
        print(
            f"Time {end_time - start_time:.2f} seconds. Score: {score}/{len(self.random_queries)}"
        )

    #        self.assertGreaterEqual(score, len(self.random_queries))

    def test_uncommon_exact_metaphone(self):
        start_time = time.time()

        score = 0
        for query, real_name in self.queries["uncommon"]:
            node = self._search_node(query, self.finder.search_node_metaphone)
            if node and node[0] == real_name.lower():
                score += 1

        end_time = time.time()
        print(
            f"Time {end_time - start_time:.2f} seconds. Score: {score}/{len(self.queries['uncommon'])}"
        )

    def test_random_search_lev_double_metaphone(self):
        start_time = time.time()

        score = 0
        for query, real in self.random_queries:
            node = self._search_node(
                query, self.finder.search_node_lev_double_metaphone
            )
            if node and node[0] == real.lower():
                score += 1

        end_time = time.time()
        print(
            f"Time {end_time - start_time:.2f} seconds. Score: {score}/{len(self.random_queries)}"
        )

    def test_uncommon_search_lev_double_metaphone(self):
        start_time = time.time()

        score = 0
        for query, real_name in self.queries["uncommon"]:
            node = self._search_node(
                query, self.finder.search_node_lev_double_metaphone
            )
            if node and node[0] == real_name.lower():
                score += 1

        end_time = time.time()
        print(
            f"Time {end_time - start_time:.2f} seconds. Score: {score}/{len(self.queries['uncommon'])}"
        )

    def test_random_fuzzy_metaphone(self):
        start_time = time.time()

        score = 0
        for query, real in self.random_queries:
            node = self._search_node(query, self.finder.search_node_fuzzy_metaphone)
            if node and node[0] == real.lower():
                score += 1

        end_time = time.time()
        print(
            f"Time {end_time - start_time:.2f} seconds. Score: {score}/{len(self.random_queries)}"
        )

    #        self.assertGreaterEqual(score, len(self.random_queries))

    def test_uncommon_fuzzy_metaphone(self):
        start_time = time.time()

        score = 0
        for query, real_name in self.queries["uncommon"]:
            node = self._search_node(query, self.finder.search_node_fuzzy_metaphone)
            if node and node[0] == real_name.lower():
                score += 1

        end_time = time.time()
        print(
            f"Time {end_time - start_time:.2f} seconds. Score: {score}/{len(self.queries['uncommon'])}"
        )


#        self.assertGreaterEqual(score, len(self.queries["uncommon"]))


if __name__ == "__main__":
    unittest.main()
