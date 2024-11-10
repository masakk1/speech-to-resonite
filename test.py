from src.phonetic_fuzz_search import PhoneticFuzzSearch

engine = PhoneticFuzzSearch("data/dictionaries/resonite-node-database.json")
engine.debug = True

search = engine._search_template()

print("float -> float")
print(engine.search_type_fuzzy_metaphone("float"))

print("float two -> float2")
print(engine.search_type_fuzzy_metaphone("float two"))

print("double two x two -> double2x2")
print(engine.search_type_fuzzy_metaphone("double two x two"))

print("u int to -> uint2")
print(engine.search_type_fuzzy_metaphone("u int to"))
