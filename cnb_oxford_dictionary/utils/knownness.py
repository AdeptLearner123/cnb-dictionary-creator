from cnb_oxford_dictionary.utils.definitions import is_proper

PROPER_KNOWNNESS = 0.7
KNOWNNESS_PER_SENT = 0.1

def get_knownness(entry, sentence_count):
    if is_proper(entry):
        return PROPER_KNOWNNESS
    return min(1, sentence_count * KNOWNNESS_PER_SENT)