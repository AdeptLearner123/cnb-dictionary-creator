def append_period(sentence):
    if sentence[-1] != ".":
        return sentence + "."
    return sentence


def get_definition_text(entry, sense):
    if "definitions" not in sense:
        return None

    sentences = [ sense["definitions"][0]]
    if "notes" in entry:
        for note in entry["notes"]:
            if note["type"] == "encyclopedicNote":
                sentences.append(note["text"])

    text = " ".join([ append_period(sentence) for sentence in sentences]).strip()
    return text