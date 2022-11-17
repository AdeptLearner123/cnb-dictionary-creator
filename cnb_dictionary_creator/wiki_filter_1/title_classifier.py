IGNORE_TOKENS = ["the", "of", "-"]


def title_is_short_entity(title):
    label = None
    if "_(" in title:
        pieces = title.split("_(")
        title = pieces[0]
        labels = pieces[1:]
        # Trim closing parentheses from label
        labels = [label[:-1] for label in labels]

    tokens = title.replace("-", "_").split("_")
    tokens = [token for token in tokens if token.lower() not in IGNORE_TOKENS]

    return len(tokens) <= 2
