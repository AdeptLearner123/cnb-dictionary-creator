from .cardword_token_merger import CardwordTokenMerger

SPLIT_TOKENS = ["-", ","]

cardwords_merger = CardwordTokenMerger()

def tokenize(text):
    for split_token in SPLIT_TOKENS:
        text = text.replace(split_token, " ")
    tokens = text.split(" ")
    tokens = [ token.upper() for token in tokens if len(token) > 0 ]
    return cardwords_merger.merge(tokens)