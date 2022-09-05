import json
from dataclasses import asdict, dataclass

# read files

with open("cache/merged.json", "r") as input_:
    merged = json.load(input_)

with open("cache/business_.json", "r") as input_:
    business = json.load(input_)

# setup for db

@dataclass
class Word:
    text: str
    usable: True


business = set(business)

words = [Word(word, word in business) for word in merged]

# save

with open("cache/words.json", "w") as output:
    json.dump([asdict(word) for word in words], output, indent=4)

print("Alles:", len(merged))
print("Business:", len(business))