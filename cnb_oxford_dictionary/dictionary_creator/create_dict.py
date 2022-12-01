
from cnb_oxford_dictionary.download.caches import DefinitionsCache, SentencesCache
from cnb_oxford_dictionary.utils.definition import get_definition_text
from cnb_oxford_dictionary.utils.get_pos import get_pos
from cnb_oxford_dictionary.utils.cross_references import get_cross_references
from cnb_oxford_dictionary.utils.senses import iterate_senses
from cnb_oxford_dictionary.utils.word_forms import get_word_forms
from cnb_oxford_dictionary.utils.sentences import get_sense_sentence_counts
from cnb_oxford_dictionary.utils.knownness import get_knownness
from cnb_oxford_dictionary.utils.sem_links import get_sem_links
from config import WORD_FREQ_FILTERED, DICTIONARY

import json

LEXICAL_CATEGORIES = set(["adjective", "verb", "noun", "numeral", "proper"])


def main():
    with open(WORD_FREQ_FILTERED, "r") as file:
        words = file.read().splitlines()

    definitions_cache = DefinitionsCache()
    sentences_cache = SentencesCache()

    sentence_counts = get_sense_sentence_counts(sentences_cache)
    cross_references = get_cross_references(definitions_cache)

    dictionary = dict()

    for result, lexical_entry, entry, sense, word in iterate_senses(definitions_cache, words):
        pos = get_pos(lexical_entry, entry)
        
        if pos not in LEXICAL_CATEGORIES:
            continue

        dictionary[sense["id"]] = {
            "word": word,
            "pos": pos,
            "definition": get_definition_text(entry, sense),
            "knownness": get_knownness(entry, sentence_counts[sense["id"]]),
            "wordForms": get_word_forms(result, lexical_entry, entry, sense, cross_references),
            "semLinks": get_sem_links(sense)
        }

    with open(DICTIONARY, "w+") as file:
        file.write(
            json.dumps(dictionary, indent=4, ensure_ascii=False)
        )


if __name__ == "__main__":
    main()