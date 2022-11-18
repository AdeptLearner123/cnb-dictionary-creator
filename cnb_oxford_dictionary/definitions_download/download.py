import json
from cnb_oxford_dictionary.download.api_downloader import download
from cnb_oxford_dictionary.download.caches import DefinitionsCache
from config import WORD_FREQ_FILTERED, MISSING_DEFINITIONS

from argparse import ArgumentParser
import os

URL = "https://od-api.oxforddictionaries.com/api/v2/words/en-us"
CHUNK_SIZE = 5

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--app-id", type=str, required=True)
    parser.add_argument("--app-key", type=str, required=True)
    args = parser.parse_args()
    return args.app_id, args.app_key


def get_request_params(word, app_id, app_key):
    return {
        "url": URL,
        "headers": {"app_id": app_id, "app_key": app_key},
        "params": {"q": word},
    }


def process_result(key, result):
    if result.status_code != 200:
        print(
            "Invalid status code for",
            key,
            result.status_code,
            result.text,
        )
        with open(MISSING_DEFINITIONS, "a") as file:
            file.write(key + "\n")
        return None, True

    return json.dumps(result.json()), True


def main():
    with open(WORD_FREQ_FILTERED, "r") as file:
        words = file.read().splitlines()
    
    if os.path.isfile(MISSING_DEFINITIONS):
        with open(MISSING_DEFINITIONS, "r") as file:
            missing_definitions = set(file.read().splitlines())
            words = [word for word in words if word not in missing_definitions]

    app_id, app_key = parse_args()

    download(
        keys=words,
        get_request_params=lambda word: get_request_params(
            word, app_id, app_key
        ),
        cache=DefinitionsCache(),
        process_result=process_result,
        chunk_size=CHUNK_SIZE,
        download_rate=1,  # Oxford API limits usage to 1 request / second
    )


if __name__ == "__main__":
    main()
