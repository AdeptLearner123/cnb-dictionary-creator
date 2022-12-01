from tqdm import tqdm
import json
from collections import defaultdict

def sense_has_def(sense_json):
    return "id" in sense_json and "definitions" in sense_json


def iterate_senses(definitions_cache, queries=None, filter_def=True):
    query_to_result = definitions_cache.get_key_to_value()
    
    if queries is None:
        queries = tqdm(list(query_to_result.keys()))

    for query in queries:
        if query not in query_to_result:
            continue

        results_str = query_to_result[query]
        results = json.loads(results_str)
        for result in results["results"]:
            for lexical_entry in result["lexicalEntries"]:
                for entry in lexical_entry["entries"]:
                    if "senses" in entry:
                        for sense in entry["senses"]:
                            if not filter_def or sense_has_def(sense):
                                yield result, lexical_entry, entry, sense, query

                            if "subsenses" in sense:
                                for subsense in sense["subsenses"]:
                                    if not filter_def or sense_has_def(subsense):
                                        yield result, lexical_entry, entry, subsense, query


def get_wordform_notes(sense):
    if "notes" in sense:
        return [ item["text"].replace("\"", "") for item in sense["notes"] if item["type"] == "wordFormNote" ]
    return []


def get_cross_references(definitions_cache):
    cross_references = defaultdict(lambda: [])

    for result, lexical_entry, entry, sense, _ in iterate_senses(definitions_cache, filter_def=False):
        if "crossReferences" not in sense:
            continue
        cross_reference_ids = [ item["id"] for item in sense["crossReferences"] ]

        reference_texts = get_wordform_notes(sense)
        if len(reference_texts) == 0:
            reference_texts = [ lexical_entry["text"] ]

        for cross_reference_id in cross_reference_ids:
            cross_references[cross_reference_id] += reference_texts
    
    return cross_references


def get_sense_to_entry(definitions_cache):
    sense_to_entry = dict()

    for result, lexical_entry, entry, sense, _ in iterate_senses(definitions_cache):
        sense_id = sense["id"]
        sense_to_entry[sense_id] = (result, lexical_entry, entry, sense)
    
    return sense_to_entry


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

    if "domainClasses" in sense:
        domain = sense["domainClasses"][0]["text"]
        text = f"({domain}) {text}"
    
    return text


def is_proper(entry):
    if "grammaticalFeatures" not in entry:
        return False
    grammatical_features = [ item["id"] for item in entry["grammaticalFeatures"] ]
    return "proper" in grammatical_features