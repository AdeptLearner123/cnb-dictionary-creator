import os

from wordfreq import word_frequency

from config import WORD_FREQ_FILTERED, ALL_LEMMAS

# wordfreq is generally unreliable, for example "handgrip" has a very low frequency
FREQUENCY_THRESHOLD = 0


def main():
    with open(ALL_LEMMAS, "r") as file:
        lemmas = file.read().splitlines()

    lemmas = [ lemma for lemma in lemmas if word_frequency(lemma, "en") > FREQUENCY_THRESHOLD ]

    with open(WORD_FREQ_FILTERED, "w+") as file:
        file.write("\n".join(lemmas))


if __name__ == "__main__":
    main()
