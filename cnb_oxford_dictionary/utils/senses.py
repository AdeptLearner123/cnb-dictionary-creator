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


def get_sense_to_entry(definitions_cache):
    sense_to_entry = dict()

    for result, lexical_entry, entry, sense, _ in iterate_senses(definitions_cache):
        sense_id = sense["id"]
        sense_to_entry[sense_id] = (result, lexical_entry, entry, sense)
    
    return sense_to_entry