import requests
from bs4 import BeautifulSoup


def _get_slugified(tag):
    try:
        return tag["href"].split("/")[-2]
    except Exception:
        pass
    return None


def search_card(set_slug, card_number=None):
    filters = [f"set:{set_slug}"]
    if card_number:
        filters.append(f"number:{card_number}")

    results = []

    r = requests.get(
        "https://pkmncards.com/",
        params={
            "s": " ".join(filters),
            "display": "full",
            "sort": "number",
            "order": "asc",
        },
    )

    items = BeautifulSoup(r.text, "html.parser").find_all("article")

    for num, item in enumerate(items, 1):
        card = {
            "name": item.find("a", {"class": "name"}).text,
            "number": num if not card_number else card_number,
            "image": item.find("img", {"class": "wp-post-image"})["src"].split("?")[0],
        }

        illustrator_link = item.find("a", {"class": "artist"})
        if illustrator_link:
            card["illustrator"] = illustrator_link.text.strip()

        for key in ["rarity", "type", "stage", "hp", "color"]:
            value = _get_slugified(item.find("a", {"class": key}))
            card[key] = value

        if card["stage"]:
            card["type"] = "pokemon"
        if card["hp"]:
            card["hp"] = int(card["hp"])

        results.append(card)

    return results


if __name__ == "__main__":
    import json

    r = search_card("fossil", 45)

    print(json.dumps(r, indent=4))
