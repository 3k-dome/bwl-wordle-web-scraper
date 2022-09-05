import argparse
import json
import random
import string
from functools import partial
from time import sleep
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

# arg parser

parser = argparse.ArgumentParser()
parser.add_argument("--min", type=int, required=True, help="min. wordlength as integer.")
parser.add_argument("--max", type=int, required=True, help="max. wordlength as integer.")
args = parser.parse_args()

# get each list of  words


def get_all_german_words() -> List[str]:
    """Simply downloads the wordlist from Netzmafia."""
    words: List[str] = []
    response = requests.get("http://www.netzmafia.de/software/wordlists/deutsch.txt")
    for line in response.text.splitlines():
        word = line.strip().lower()
        words.append(word)
    return words


def get_all_business_words() -> List[str]:
    """Get all words from Gabler."""
    word_list: List[str] = []
    base_url = "https://wirtschaftslexikon.gabler.de/"
    link = "/definition-a-z/a-z"

    def get_business_page(url: str) -> Optional[str]:
        """This iterates over each page of the search and moves to the next if any."""
        print(f"Getting: {url}")
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        word_list.extend([keyword.text.strip().lower() for keyword in soup.find_all(class_="keyword")])
        try:
            return soup.find("a", {"title": "Zur nächsten Seite"})["href"]  # type: ignore
        except Exception:
            return None

    # as long as a new page is found we parse it
    # the sleeps makes us look like a human ;)
    while link:
        link = get_business_page(f"{base_url}{link}")
        sleep(random.uniform(1, 5))
    return word_list


german_words = get_all_german_words()
business_words = get_all_business_words()

# filter both lists


def filter_by_punctuation(word_list: List[str]) -> List[str]:
    """Filters a list of strings by any punctuation character."""
    punctuation = set(string.punctuation)

    def punctuation_filter(word: str) -> bool:
        for letter in word:
            if letter in punctuation:
                return False
        return True

    return [*filter(punctuation_filter, word_list)]


def filter_by_spaces(word_list: List[str]) -> List[str]:
    """Filters a list of strings by any spaces."""

    def spaces_filter(word: str) -> bool:
        return False if word.__contains__(" ") else True

    return [*filter(spaces_filter, word_list)]


german_words = filter_by_punctuation(german_words)
german_words = filter_by_spaces(german_words)

business_words = filter_by_punctuation(business_words)
business_words = filter_by_spaces(business_words)

# transform sonderzeichen both lists


def replace_sonderzeichen(word_list: List[str]) -> None:
    """Transform each sonderzeichen by mutating a list of strings."""
    for i, word in enumerate(word_list):
        word = word.replace("ß", "ss")
        word = word.replace("ü", "ue")
        word = word.replace("ö", "oe")
        word = word.replace("ä", "ae")
        word_list[i] = word


replace_sonderzeichen(german_words)
replace_sonderzeichen(business_words)

# filter by length


def filter_by_length(word_list: List[str], *, min: int, max: int) -> List[str]:
    def length_filter(word: str, min: int, max: int) -> bool:
        if word.__len__() <= max and word.__len__() >= min:
            return True
        return False

    return [*filter(partial(length_filter, min=min, max=max), word_list)]


german_words = filter_by_length(german_words, min=args.min, max=args.max)
business_words = filter_by_length(business_words, min=args.min, max=args.max)

# save both sets

merged = set([*german_words, *business_words])

with open("cache/merged.json", "w") as output:
    json.dump([*merged], output, indent=4)

with open("cache/business.json", "w") as output:
    json.dump([*business_words], output, indent=4)
