from cnb_oxford_dictionary.utils.tokenizer import tokenize
from cnb_oxford_dictionary.utils.definitions import is_proper
from wordfreq import word_frequency

LEXICAL_CATEGORIES = set(["adjective", "verb", "noun"])


def get_clue_variants(json):
    if "variantForms" not in json:
        return []
    
    variants = [ variant_form["text"].upper() for variant_form in json["variantForms"] ]
    variants = [ variant for variant in variants if len(tokenize(variant)) == 1 ]
    return variants


def extract_clue_tokens(lexical_entry, entry, sense):
    word = lexical_entry["text"]
    lexical_category = lexical_entry["lexicalCategory"]["id"]
    
    if lexical_category not in LEXICAL_CATEGORIES:
        return None
    
    clue_tokens = []
    tokens = tokenize(word)
    if len(tokens) == 1:
        clue_tokens += tokens

    clue_variants = get_clue_variants(entry) + get_clue_variants(sense)
    clue_tokens += clue_variants

    if len(clue_tokens) > 0:
        return clue_tokens

    if is_proper(entry):
        if ", " in word:
            # Is a person's name
            return [ tokens[0] ,tokens[-1] ]
        elif len(tokens) == 2:
            # If proper compound is only two words, choose the rarer one
            return [ min(tokens, key=lambda token: word_frequency(token.lower(), "en")) ]
    
    return None