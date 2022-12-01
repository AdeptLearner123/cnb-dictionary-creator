from collections import defaultdict
from .senses import iterate_senses

def get_wordform_notes(sense):
    if "notes" in sense:
        return [ item["text"].replace("\"", "") for item in sense["notes"] if item["type"] == "wordFormNote" ]
    return []


def get_cross_references(definitions_cache):
    cross_references = defaultdict(lambda: [])

    for _, lexical_entry, _, sense, _ in iterate_senses(definitions_cache, filter_def=False):
        if "crossReferences" not in sense:
            continue
        cross_reference_ids = [ item["id"] for item in sense["crossReferences"] ]

        reference_texts = get_wordform_notes(sense)
        if len(reference_texts) == 0:
            reference_texts = [ lexical_entry["text"] ]

        for cross_reference_id in cross_reference_ids:
            cross_references[cross_reference_id] += reference_texts
    
    return cross_references
