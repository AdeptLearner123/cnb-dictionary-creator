def get_sem_links(sense):
    sem_links = dict()

    if "domainClasses" in sense:
        sem_links["domains"] = [domain_class["text"].replace("_", " ").lower() for domain_class in sense["domainClasses"]]

    if "semanticClasses" in sense:
        sem_links["classes"] = [semantic_class["text"].replace("_", " ").lower() for semantic_class in sense["semanticClasses"]]

    if "synonyms" in sense:
        sem_links["synonyms"] = [synonym["text"] for synonym in sense["synonyms"]]
    
    return sem_links