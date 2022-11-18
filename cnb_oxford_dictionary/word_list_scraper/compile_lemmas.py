import os

from config import ALL_LEMMAS, SCRAPED_LEMMAS_DIR, SCRAPED_LEMMAS_DIR


def main():
    lemmas = set()

    for file_name in os.listdir(SCRAPED_LEMMAS_DIR):
        with open(os.path.join(SCRAPED_LEMMAS_DIR, file_name), "r") as file:
            lemmas = file.read().splitlines()
            lemmas = set(map(lambda lemma: lemma.lower(), lemmas))

    lemmas = list(lemmas)
    with open(ALL_LEMMAS, "w+") as file:
        file.write("\n".join(lemmas))


if __name__ == "__main__":
    main()
