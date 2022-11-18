from config import (
    SCRAPED_INDICES_DIR,
    SCRAPED_LEMMAS_DIR,
)

from .indices_scraper import scrape_indices
from .lemmas_scraper import scrape_lemmas


def main():
    scrape_indices(SCRAPED_INDICES_DIR, "american_english")

    scrape_lemmas(
        SCRAPED_INDICES_DIR,
        SCRAPED_LEMMAS_DIR,
        "american_english",
    )


if __name__ == "__main__":
    main()
