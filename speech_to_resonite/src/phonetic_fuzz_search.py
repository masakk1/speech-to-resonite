import json
from rapidfuzz import process
import metaphone


class PhoneticFuzzSearch:

    def __init__(self, database_path="dictionaries/resonite-node-database.json"):
        self.debug = False

        self.database_path = database_path
        self.get_database()

    def debugging_print(self, *args, **kwargs):
        if self.debug:
            print(*args, **kwargs)

    def get_database(self):
        with open(self.database_path, "r") as f:
            self.database = json.load(f)

        self.nodes = self.database["nodes"]

    def search_fuzzy(self, query: str, list, limit) -> list:
        return process.extract(query, list, limit=limit)

    def search_node_metaphone(self, query: str, list, limit=5) -> list:
        query_metaphone = metaphone.doublemetaphone(query)

        self.debugging_print(f"Query: {query}, metaphone: {query_metaphone}")

        matches = []
        index = 0
        for item in list:
            if index >= limit:
                break
            if item["metaphone0"] == query_metaphone[0]:
                self.debugging_print(
                    f"looking at {item["name"]} - metaphone: {item['metaphone0']}"
                )
                matches.append(item)
                index += 1

        return matches

    def search_node(self, query: str):
        query = query.lower()
        found_node = None

        metaphone_matches = self.search_node_metaphone(query, self.nodes, 5)
        self.debugging_print("Phonetic matches:", metaphone_matches)
        if metaphone_matches == []:
            self.debugging_print(
                f"No metaphone matches found for {query} ({metaphone.dm(query)})"
            )
            return None

        fuzzy_matches = self.search_fuzzy(
            query, [node["name"].lower() for node in metaphone_matches], limit=20
        )
        self.debugging_print("Fuzzy matches:", fuzzy_matches)
        found_node = fuzzy_matches[0]

        return found_node[0]
