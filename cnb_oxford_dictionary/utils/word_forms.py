def get_word_forms(result, lexical_entry, entry, sense, cross_references):
    variants = [ format_text(lexical_entry["text"]) ]
    variants += cross_references[result["id"]]
    variants += extract_json_variants(entry) + extract_json_variants(sense)
    variants += get_entry_inflections(entry)
    return list(set(variants))


def format_text(text):
    if ", " in text and text.count(", ") == 1:
        last, first = text.split(", ")
        return " ".join([first, last])
    return text


def extract_json_variants(json):
    if "variantForms" not in json:
        return []
    
    return [ variant_form["text"] for variant_form in json["variantForms"] ]


def get_entry_inflections(entry):
    if "inflections" in entry:
        return [
            inflection["inflectedForm"]
            for inflection in entry["inflections"]
        ]
    return []