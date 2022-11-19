import os
import json

from config import TESTS_DATA
from cnb_oxford_dictionary.clue_filter.clue_tokens_extractor import extract_clue_tokens
from cnb_oxford_dictionary.utils.definitions import get_sense_to_entry
from cnb_oxford_dictionary.download.caches import DefinitionsCache
from cnb_oxford_dictionary.clue_filter.clue_tokens_extractor import extract_clue_tokens

def test_clue_tokens_extractor():
    with open(os.path.join(TESTS_DATA, "clue_tokens_extractor.json")) as file:
        test_data = json.loads(file.read())

    definitions_cache = DefinitionsCache()
    sense_to_entry = get_sense_to_entry(definitions_cache)

    for sense_id, expected_tokens in test_data.items():
        tokens = set(extract_clue_tokens(*sense_to_entry[sense_id]))
        expected_tokens = set(expected_tokens)
        assert (
            expected_tokens == tokens
        ), f"Expected {sense_id} to have tokens {expected_tokens} but was {tokens}"
