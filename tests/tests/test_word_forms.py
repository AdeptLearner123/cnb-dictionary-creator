import os
import json

from config import TESTS_DATA
from cnb_oxford_dictionary.utils.word_forms import get_word_forms
from cnb_oxford_dictionary.utils.senses import get_sense_to_entry
from cnb_oxford_dictionary.utils.cross_references import get_cross_references
from cnb_oxford_dictionary.download.caches import DefinitionsCache

def test_clue_tokens_extractor():
    with open(os.path.join(TESTS_DATA, "word_forms.json")) as file:
        test_data = json.loads(file.read())

    definitions_cache = DefinitionsCache()
    sense_to_entry = get_sense_to_entry(definitions_cache)
    cross_references = get_cross_references(definitions_cache)

    for sense_id, expected_word_forms in test_data.items():
        word_forms = set(get_word_forms(*sense_to_entry[sense_id], cross_references))
        expected_word_forms = set(expected_word_forms)
        assert (
            expected_word_forms == word_forms
        ), f"Expected {sense_id} to have tokens {expected_word_forms} but was {word_forms}"