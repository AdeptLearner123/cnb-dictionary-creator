import json
from cnb_oxford_dictionary.download.api_downloader import download
from cnb_oxford_dictionary.download.caches import SentencesCache
from cnb_oxford_dictionary.utils.definitions import iterate_senses
from config import CLUE_TOKEN_FILTERED, COMPOUND_CLUE_FILTERED, MISSING_SENTENCES
from argparse import ArgumentParser

import os

GET_URL = (
    lambda word: f"https://od-api.oxforddictionaries.com/api/v2/sentences/en/{word}?strictMatch=false"
)
CHUNK_SIZE = 5

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--app-id", type=str, required=True)
    parser.add_argument("--app-key", type=str, required=True)
    args = parser.parse_args()
    return args.app_id, args.app_key


def get_request_params(word, app_id, app_key):
    return {
        "url": GET_URL(word),
        "headers": {
            "Accept": "application/json",
            "app_id": app_id,
            "app_key": app_key,
        },
    }


def process_result(key, result):
    if result.status_code != 200:
        print("Missing", key)
        with open(MISSING_SENTENCES, "a+") as file:
            file.write(key + "\n")
        return None, True

    if result.status_code != 200:
        print(
            "Invalid status code for",
            key,
            result.status_code,
            result.text,
        )
        return None, False

    return json.dumps(result.json()), True


def main():
    words = set()

    with open(CLUE_TOKEN_FILTERED, "r") as file:
        words.update([ item["word"] for item in json.loads(file.read()).values() ])

    with open(COMPOUND_CLUE_FILTERED, "r") as file:
        words.update([ item["word"] for item in json.loads(file.read()).values() ])

    if os.path.isfile(MISSING_SENTENCES):
        with open(MISSING_SENTENCES, "r") as file:
            missing_sentences = set(file.read().splitlines())
            words = list(filter(lambda word: word not in missing_sentences, words))

    app_id, app_key = parse_args()

    download(
        keys=words,
        get_request_params=lambda word: get_request_params(word, app_id, app_key),
        cache=SentencesCache(),
        process_result=process_result,
        chunk_size=CHUNK_SIZE,
        download_rate=1,  # Oxford API limits usage to 1 request / second
    )


if __name__ == "__main__":
    main()
