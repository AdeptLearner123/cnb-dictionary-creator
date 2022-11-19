from cnb_oxford_dictionary.utils.tokenizer import tokenize
from wordfreq import word_frequency

LEXICAL_CATEGORIES = set(["adjective", "verb", "noun"])


def get_clue_variants(json):
    if "variantForms" not in json:
        return []
    
    variants = [ variant_form["text"] for variant_form in json["variantForms"] ]
    variants = [ variant for variant in variants if len(tokenize(variant)) == 1 ]
    return variants


def is_proper(entry):
    if "grammaticalFeatures" not in entry:
        return False
    grammatical_features = [ item["id"] for item in entry["grammaticalFeatures"] ]
    return "proper" in grammatical_features


def extract_clue_tokens(lexical_entry, entry, sense):
    word = lexical_entry["text"]
    lexical_category = lexical_entry["lexicalCategory"]["id"]
    
    if lexical_category not in LEXICAL_CATEGORIES:
        return None
    
    tokens = tokenize(word)
    if len(tokens) == 1:
        return tokens

    clue_variants = get_clue_variants(entry) + get_clue_variants(sense)
    if len(clue_variants) > 0:
        return clue_variants

    if is_proper(entry):
        if ", " in word:
            # Is a person's name
            return [ tokens[0] ,tokens[-1] ]
        elif len(tokens) == 2:
            # If proper compound is only two words, choose the rarer one
            return [ min(tokens, key=lambda token: word_frequency(token.lower(), "en")) ]
    
    return None