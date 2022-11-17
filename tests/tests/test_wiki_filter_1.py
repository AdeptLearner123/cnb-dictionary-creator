import os
import json

from config import TESTS_DATA
from cnb_dictionary_creator.wiki_filter_1.title_classifier import title_is_short_entity


def test_wiki_filter_1():
    with open(os.path.join(TESTS_DATA, "wiki_filter_1.json")) as file:
        test_data = json.loads(file.read())

    for title, label in test_data.items():
        assert title_is_short_entity(title) == label
