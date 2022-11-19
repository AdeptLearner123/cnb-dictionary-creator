from config import WORD_FREQ_FILTERED, COMPOUND_CLUE_FILTERED, CARDWORDS
from cnb_oxford_dictionary.download.caches import DefinitionsCache
from cnb_oxford_dictionary.utils.definitions import iterate_senses
from cnb_oxford_dictionary.utils.tokenizer import tokenize

import json


def extract_compound_tokens(word):
    tokens = tokenize(word)

    if len(tokens) != 2:
        return None

    return tokens


def main():
    with open(WORD_FREQ_FILTERED, "r") as file:
        words = file.read().splitlines()

    with open(CARDWORDS, "r") as file:
        cardwords = file.read().splitlines()

    definitions_cache = DefinitionsCache()
    compound_tokens = dict()

    for lexical_entry, _, sense, word in iterate_senses(definitions_cache, words):
        tokens = extract_compound_tokens(lexical_entry["text"])

        if tokens is not None and any([token.upper() in cardwords for token in tokens]):
            compound_tokens[sense["id"]] = {
                "tokens": tokens,
                "word": word
            }

    with open(COMPOUND_CLUE_FILTERED, "w+") as file:
        file.write(
            json.dumps(compound_tokens, indent=4, sort_keys=True, ensure_ascii=False)
        )


if __name__ == "__main__":
    main()
