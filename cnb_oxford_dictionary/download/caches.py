from .cache import Cache
from config import (
    DEFINITIONS_CACHE,
    SENTENCES_CACHE
)


class DefinitionsCache(Cache):
    def __init__(self):
        super().__init__(DEFINITIONS_CACHE, False)


class SentencesCache(Cache):
    def __init__(self):
        super().__init__(SENTENCES_CACHE, False)
