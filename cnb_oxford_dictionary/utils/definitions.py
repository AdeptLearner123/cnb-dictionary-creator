from tqdm import tqdm
import json

def sense_has_def(sense_json):
    return "id" in sense_json and "definitions" in sense_json


def iterate_senses(definitions_cache, queries=None):
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
                            if sense_has_def(sense):
                                yield lexical_entry, entry, sense, query

                            if "subsenses" in sense:
                                for subsense in sense["subsenses"]:
                                    if sense_has_def(subsense):
                                        yield lexical_entry, entry, subsense, query


def get_sense_to_entry(definitions_cache):
    sense_to_entry = dict()

    for lexical_entry, entry, sense, _ in iterate_senses(definitions_cache):
        sense_id = sense["id"]
        sense_to_entry[sense_id] = (lexical_entry, entry, sense)
    
    return sense_to_entry