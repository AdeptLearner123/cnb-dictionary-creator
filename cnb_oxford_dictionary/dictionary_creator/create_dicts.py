
from cnb_oxford_dictionary.download.caches import DefinitionsCache, SentencesCache
from cnb_oxford_dictionary.utils.definitions import get_sense_to_entry, get_definition_text
from cnb_oxford_dictionary.utils.sentences import get_sense_sentence_counts
from cnb_oxford_dictionary.utils.knownness import get_knownness
from config import CLUE_TOKEN_FILTERED, COMPOUND_CLUE_FILTERED, SEM_LINK_FILTERED, CLUE_TOKEN_DICT, COMPOUND_DICT, SEM_LINK_DICT

import json

def create_dict(DICT_PATH, OUTPUT_PATH, sentence_counts, sense_to_entry):
    with open(DICT_PATH, "r") as file:
        dictionary = json.loads(file.read())
    
    new_dictionary = dict()

    for sense_id, dict_entry in dictionary.items():
        _, _, entry, sense = sense_to_entry[sense_id]

        new_dictionary[sense_id] = {
            **dict_entry,
            "definition": get_definition_text(entry, sense),
            "knownness": get_knownness(entry, sentence_counts[sense_id])
        }
    
    with open(OUTPUT_PATH, "w+") as file:
        file.write(json.dumps(new_dictionary, indent=4, sort_keys=True, ensure_ascii=False))


def main():
    definitions_cache = DefinitionsCache()
    sentences_cache = SentencesCache()

    sentence_counts = get_sense_sentence_counts(sentences_cache)
    sense_to_entry = get_sense_to_entry(definitions_cache)

    create_dict(CLUE_TOKEN_FILTERED, CLUE_TOKEN_DICT, sentence_counts, sense_to_entry)
    create_dict(COMPOUND_CLUE_FILTERED, COMPOUND_DICT, sentence_counts, sense_to_entry)
    create_dict(SEM_LINK_FILTERED, SEM_LINK_DICT, sentence_counts, sense_to_entry)


if __name__ == "__main__":
    main()