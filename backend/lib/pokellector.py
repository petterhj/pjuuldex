import logging

import requests
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)


class UnknownSetException(Exception):
    pass


def get_cards(set_code):
    logger.info(f"Fetching Pokellector set {set_code}")

    r = requests.get(
        f"https://www.pokellector.com/sets/{set_code}?list_display=list",
        params={"list_display": "list"}
    )

    soup = BeautifulSoup(r.text, "html.parser")
    cards_listing = soup.find("div", class_="cardlisting")

    if not cards_listing:
        raise UnknownSetException()

    cards = {}

    for card in cards_listing.find_all("li"):
        number = int(card.find("span", class_="number").text)
        ref = card.find("a")["href"].split("/")[-1]
        cards[number] = ref

    logger.info(f"Found {len(cards)} cards")

    return cards


def get_variants(card_slug):
    r = requests.get(f"https://www.pokellector.com/card/{card_slug}")
    soup = BeautifulSoup(r.text, "html.parser")
    variants_container = soup.find("a", attrs={"name": "variants"}).find_next("div", class_="cardlisting")
    variants = [e.text.strip() for e in variants_container.find_all("div", class_="plaque")]
    return variants


if __name__ == "__main__":
    import json

    r = get_cards("BS23123-Base-Set222")
    # r = get_variants("Alakazam-Base-Set-BS-1")

    print(json.dumps(r, indent=4))
