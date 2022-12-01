def get_pos(lexical_entry, entry):
    pos = lexical_entry["lexicalCategory"]["id"]

    if is_proper(entry):
        return "proper"
    
    return pos


def is_proper(entry):
    if "grammaticalFeatures" not in entry:
        return False
    grammatical_features = [ item["id"] for item in entry["grammaticalFeatures"] ]
    return "proper" in grammatical_features
