import json
from rapidfuzz import process
import metaphone
import Levenshtein as lev


def remove_list_dulicates(ls: list) -> list:
    return list(set(ls))


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

    def search_node_fuzzy_metaphone(self, query: str, nodes, limit) -> list:
        """
        Returns a list of nodes that are the most similar(fuzzy)
        to the metaphone of the query.
        """
        query_metaphone = metaphone.doublemetaphone(query)

        self.debugging_print(f"Query: {query}, metaphone: {query_metaphone}")

        matches_metaphone = self.search_fuzzy(
            query_metaphone[0], [node["metaphone0"] for node in nodes], limit=limit
        )
        matches_metaphone = remove_list_dulicates(matches_metaphone)
        self.debugging_print("Metaphone matches:", matches_metaphone)

        matching_nodes = []
        for match in matches_metaphone:
            code, score, _ = match
            for node in nodes:
                if node["metaphone0"] == code:
                    matching_nodes.append(node)

        return matching_nodes

    def match_lev_double_metaphone(
        self, similarity_theshold, query1, query2, target1, target2
    ):
        dist11 = lev.distance(query1, target1)
        dist12 = lev.distance(query1, target2)
        dist21 = lev.distance(query2, target1)
        dist22 = lev.distance(query2, target2)

        weighted_distance = (dist11 + dist12 + dist21 + dist22) / 4

        return weighted_distance <= similarity_theshold, weighted_distance

    def search_node_lev_double_metaphone(self, query: str, nodes, limit) -> list:
        """
        Returns a list fo nodes that are most similar(levenshtein distance)
        to the metaphone(s) of the query.
        """
        query1, query2 = metaphone.doublemetaphone(query)

        self.debugging_print(f"Query: {query}, metaphone: {query1}, {query2}")

        matches = []
        for node in nodes:
            node1, node2 = node["metaphone0"], node["metaphone1"]
            is_match, distance = self.match_lev_double_metaphone(
                3, query1, query2, node1, node2
            )
            if is_match:
                matches.append(node)

        return matches

    def search_node_metaphone(self, query: str, list, limit=5) -> list:
        """
        Returns a list of nodes that exactly match
        the metaphone of the query.
        """
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
            if item["metaphone1"] != "" and item["metaphone1"] == query_metaphone[1]:
                self.debugging_print(
                    f"looking at {item['name']} - metaphone: {item['metaphone1']}"
                )
                matches.append(item)
                index += 1

        return matches

    def search_node(self, query: str):
        query = query.lower()
        found_node = None

        node_matches = self.search_node_metaphone(query, self.nodes, 5)
        self.debugging_print("Node matches:", node_matches)
        if node_matches == []:
            self.debugging_print(
                f"No metaphone matches found for {query} ({metaphone.dm(query)})"
            )
            return None

        fuzzy_matches = self.search_fuzzy(
            query, [node["name"].lower() for node in node_matches], limit=20
        )
        self.debugging_print("Fuzzy matches:", fuzzy_matches)
        found_node = fuzzy_matches[0]

        return found_node[0]
