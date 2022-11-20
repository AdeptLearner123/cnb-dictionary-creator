from collections import Counter, defaultdict
import json

def get_sense_sentence_counts(sentences_cache):
    query_to_result = sentences_cache.get_key_to_value()

    sentence_counts = defaultdict(lambda: 0)

    for results in query_to_result.values():
        sense_counts = Counter()
        for result in json.loads(results)["results"]:
            for lexical_entry in result["lexicalEntries"]:
                for sentence in lexical_entry["sentences"]:
                    for sense_id in set(sentence["senseIds"]):
                        sense_counts[sense_id] += 1
        
        # Since results might have overlapping entries, sense counts should override previous counts rather than add to them.
        sentence_counts.update(sense_counts)
    
    return sentence_counts