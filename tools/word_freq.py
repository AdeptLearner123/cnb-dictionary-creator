from wordfreq import word_frequency

from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("word", type=str)
    args = parser.parse_args()
    return args.word


def main():
    word = parse_args()
    print(word_frequency(word, "en"))
