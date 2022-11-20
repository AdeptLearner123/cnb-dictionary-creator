from config import CARDWORDS, CLUE_TOKEN_FILTERED, SEM_LINK_FILTERED
from cnb_oxford_dictionary.download.caches import DefinitionsCache
from cnb_oxford_dictionary.download.caches import SentencesCache
from cnb_oxford_dictionary.utils.definitions import get_sense_to_entry, get_definition_text
from cnb_oxford_dictionary.utils.sentences import get_sense_sentence_counts
from cnb_oxford_dictionary.utils.knownness import get_knownness
from cnb_oxford_dictionary.utils.tokenizer import tokenize

import json

def filter_links(link_texts):
    link_tokens = [ tokenize(text) for text in link_texts ]
    return [ tokens[0] for tokens in link_tokens if len(tokens) == 1 ]


def main():
    with open(CARDWORDS, "r") as file:
        cardwords = file.read().splitlines()
    with open(CLUE_TOKEN_FILTERED, "r") as file:
        sense_clue_tokens = json.loads(file.read())

    definitions_cache = DefinitionsCache()
    sense_to_entry = get_sense_to_entry(definitions_cache)
    sem_link_dict = dict()

    for sense_id in sense_clue_tokens:
        clue_tokens = sense_clue_tokens[sense_id]["tokens"]
        word = sense_clue_tokens[sense_id]["word"]
        _, _, sense = sense_to_entry[sense_id]
        sem_links = dict()

        if "domainClasses" in sense:
            domains = [domain_class["text"].replace("_", " ").upper() for domain_class in sense["domainClasses"]]
            domains = filter_links(domains)
            if len(domains) > 0:
                sem_links["DOMAIN"] = domains

        if "semanticClasses" in sense:
            classes = [semantic_class["text"].replace("_", " ").upper() for semantic_class in sense["semanticClasses"]]
            classes = filter_links(classes)
            if len(classes) > 0:
                sem_links["CLASS"] = classes

        if "synonyms" in sense:
            synonyms = [synonym["text"].upper() for synonym in sense["synonyms"]]
            if word in synonyms:
                synonyms.remove(word)
            synonyms = filter_links(synonyms)
            if len(synonyms) > 0:
                sem_links["SYNONYM"] = synonyms
        
        sem_link_tokens = sum(sem_links.values(), [])
        sem_link_tokens = [ token.upper() for token in sem_link_tokens ]

        if any([ token in cardwords for token in clue_tokens + sem_link_tokens ]):
            sem_link_dict[sense_id] = {
                "tokens": clue_tokens,
                "links": sem_links,
                "word": word,
            }
    
    with open(SEM_LINK_FILTERED, "w+") as file:
        file.write(json.dumps(sem_link_dict, indent=4, sort_keys=True, ensure_ascii=False))


if __name__ == "__main__":
    main()