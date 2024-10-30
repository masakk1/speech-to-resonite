import json
import re
import sys
import os
from num2words import num2words
from metaphone import metaphone, doublemetaphone


def convert_numbers_to_words(input_string):
    def replace_number(match):
        number = match.group(0)  # Get the matched number
        return num2words(number)  # Convert to words

    output_string = re.sub(r"\d+", replace_number, input_string)

    return output_string


def split_node_path(node_path):
    node_type_split = node_path.split("<")
    node_path_without_contents = node_type_split[0]

    parts = node_path_without_contents.split(".")

    has_type = False
    if len(node_type_split) > 1:
        node_content = "<" + node_type_split[1]
        parts.append(node_content)
        has_type = True

    return parts, has_type


def split_word_by_uppercase(words_string):
    words_string = words_string.replace("_", " ")
    return re.sub(r"(?<=[a-z])(?=[A-Z])", " ", words_string).lower().split()


def generate_nodes_grammar(funnystring):
    data = []
    parts = funnystring.split("|")

    for node_path in parts:
        if node_path == "":
            continue

        node_parts, has_type = split_node_path(node_path)
        node_name = node_parts[-2] if has_type else node_parts[-1]

        words = split_word_by_uppercase(node_name)
        for word in words:
            if not word in data:
                data.append(word)

    return data


def get_metaphone_code(string):
    string = string.replace("_", "").lower()
    string = convert_numbers_to_words(string)
    # print(string)
    code = doublemetaphone(string)
    return code


def generate_node_names(funnystring):
    data = []
    parts = funnystring.split("|")

    for node_path in parts:
        if node_path == "":
            continue

        parts, has_type = split_node_path(node_path)
        name_length = 2 if has_type else 1

        name = parts[-name_length]
        name_metaphone = get_metaphone_code(name)
        node = {
            "name": name,
            "type": parts[-1] if has_type else "",
            "metaphone0": name_metaphone[0],
            "metaphone1": name_metaphone[1],
        }

        data.append(node)

    return data


def validate_args(args):
    if len(args) < 2:
        print("Usage: python script.py <origin_file> <output_path>")
        sys.exit(1)

    if os.path.exists(args[1]) == False:
        print(f"Error: could not find the funnystring. Path = {sys.argv[1]}")
        sys.exit(1)

    if len(args) < 3:
        print("Defaulting output path to '.'")
        args.append(".")
    if os.path.exists(args[2]) == False:
        print(
            f"Error: could not find the output path. Path = {args[2]}. Defaulting position to '.'"
        )
        args[2] = "."

    return args


if __name__ == "__main__":

    args = validate_args(sys.argv)
    funnystring_path = args[1]
    with open(funnystring_path, "r") as json_file:
        funnystring = json_file.read()

    grammar = generate_nodes_grammar(funnystring)
    nodes = generate_node_names(funnystring)

    node_database = {"nodes": nodes, "grammar": grammar}

    json_data = json.dumps(node_database, indent=4)

    with open(args[2] + "/" + "resonite-node-database.json", "w") as json_file:
        json_file.write(json_data)

    print("Conversion complete. Check resonite-node-database.json for the result.")
