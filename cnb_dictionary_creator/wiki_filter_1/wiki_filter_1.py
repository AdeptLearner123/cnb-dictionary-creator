from config import WIKI_TITLES, WIKI_FILTER_1_OUTPUT

from .title_classifier import title_is_short_entity


def main():
    with open(WIKI_TITLES, "r") as file:
        titles = file.read().splitlines()

    filtered_titles = [title for title in titles if title_is_short_entity(title)]

    with open(WIKI_FILTER_1_OUTPUT, "w+") as file:
        file.write("\n".join(filtered_titles))


if __name__ == "__main__":
    main()
