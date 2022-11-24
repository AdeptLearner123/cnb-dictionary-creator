from cnb_oxford_dictionary.utils.tokenizer import tokenize
from cnb_oxford_dictionary.utils.definitions import is_proper
from wordfreq import word_frequency

LEXICAL_CATEGORIES = set(["adjective", "verb", "noun", "numeral"])

def get_clue_variants(json):
    if "variantForms" not in json:
        return []
    
    variants = [ variant_form["text"].upper() for variant_form in json["variantForms"] ]
    variants = [ variant for variant in variants if len(tokenize(variant)) == 1 ]
    return variants


def extract_clue_tokens(result, lexical_entry, entry, sense, cross_references):
    word = lexical_entry["text"]
    lexical_category = lexical_entry["lexicalCategory"]["id"]

    if lexical_category not in LEXICAL_CATEGORIES:
        return None
    
    clue_tokens = []
    tokens = tokenize(word)
    if len(tokens) == 1:
        clue_tokens += tokens

    for cross_reference in cross_references[result["id"]]:
        reference_tokens = tokenize(cross_reference)
        if len(reference_tokens) == 1:
            clue_tokens += reference_tokens

    clue_variants = get_clue_variants(entry) + get_clue_variants(sense)
    clue_tokens += clue_variants
    clue_tokens = list(set(clue_tokens))

    if is_proper(entry):
        if ", " in word:
            # Is a person's name
            clue_tokens += [ tokens[0] ,tokens[-1] ]
        elif len(tokens) == 2:
            # If proper compound is only two words, choose the rarer one
            # It should also be a significantly rare word
            rare_token = min(tokens, key=lambda token: word_frequency(token.lower(), "en"))
            if word_frequency(rare_token.lower(), "en") < 1e-4:
                clue_tokens.append(rare_token)
    
    return clue_tokens