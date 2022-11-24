from config import WORD_FREQ_FILTERED, CLUE_TOKEN_FILTERED
from cnb_oxford_dictionary.download.caches import DefinitionsCache
from cnb_oxford_dictionary.utils.definitions import iterate_senses
from .clue_tokens_extractor import extract_clue_tokens
from cnb_oxford_dictionary.utils.definitions import iterate_senses, get_cross_references

import json


def main():
    with open(WORD_FREQ_FILTERED, "r") as file:
        words = file.read().splitlines()

    definitions_cache = DefinitionsCache()
    sense_clue_tokens = dict()

    cross_references = get_cross_references(definitions_cache)

    for result, lexical_entry, entry, sense, word in iterate_senses(definitions_cache, words):
        clue_tokens = extract_clue_tokens(result, lexical_entry, entry, sense, cross_references)
        if clue_tokens is not None:
            sense_clue_tokens[sense["id"]] = {
                "tokens": clue_tokens,
                "word": word
            }

    with open(CLUE_TOKEN_FILTERED, "w+") as file:
        file.write(
            json.dumps(sense_clue_tokens, indent=4, sort_keys=True, ensure_ascii=False)
        )


if __name__ == "__main__":
    main()
