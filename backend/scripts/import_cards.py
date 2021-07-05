import os
import argparse
import logging

os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

import django
from django.db.utils import IntegrityError
from pokemontcgsdk import (
    Set as TCGSet,
    Card as TCGCard,
)

django.setup()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from scripts.util import save_image
from pokedex.models import Set, Card#, Variant, CardVariant


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-s",
        "--set",
        choices=[s.code for s in Set.objects.all()],
        required=True,
        help="Name (slug) of set to import, e.g. `base-set`",
    )
    parser.add_argument(
        "-n",
        "--card-number",
        required=False,
        help="Import specified card only",
    )
    args = parser.parse_args()
    
    tcg_set = TCGSet.find(args.set)
    card_set = Set.objects.get(code=args.set)

    if not args.card_number:
        tcg_cards = TCGCard.where(q=f"set.id:{tcg_set.id}")
    else:
        tcg_cards = [TCGCard.find(f"{tcg_set.id}-{args.card_number}")]

    logger.info("Importing {} card(s) from {}: {} (total={})".format(
        len(tcg_cards), tcg_set.id, tcg_set.name, tcg_set.printedTotal
    ))

    for tcg_card in tcg_cards:
        card = Card(
            set=card_set,
            name=tcg_card.name,
            number=int(tcg_card.number),
            supertype=tcg_card.supertype,
            subtype=",".join(tcg_card.subtypes),
            type=",".join(tcg_card.types),
            hp=tcg_card.hp,
            rarity=tcg_card.rarity,
            illustrator=tcg_card.artist,
        )

        logger.info(f"Saving card #{card.number}: {card.name} to database...")

        try:
            card.save()
            save_image(card.image, tcg_card.images.small)
        except IntegrityError:
            print("Could not save", card_set, "(IntegrityError)")

    logger.info("Done!")


"""
VARIANTS = {
    "base-set": ["first-edition", "unlimited"],
    "fossil": ["first-edition", "unlimited"],
    "jungle": ["first-edition", "unlimited"],
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-s",
        "--set",
        choices=Set.objects.values_list("slug", flat=True),
        required=True,
        help="Name (slug) of set to import, e.g. `base-set`",
    )

    args = parser.parse_args()

    card_set = Set.objects.get(slug=args.set)
    items = search_card(args.set, args.card_number)

    for item in items[0:1]:
        image_url = item.pop("image")

        # Create card
        card = Card(set=card_set, **item)
        try:
            card.save()
        except IntegrityError:
            print("Could not save", card, "(IntegrityError)")
            continue
        print(card)
        
        # Variants
        if card_set.slug in VARIANTS:
            for variant_slug in VARIANTS[card_set.slug]:
                variant = Variant.objects.filter(slug=variant_slug).first()
                card_variant = CardVariant(card=card, variant=variant)

                # Add image
                if image_url and variant_slug == "first-edition":
                    img_temp = NamedTemporaryFile(delete=True)
                    img_temp.write(urlopen(image_url).read())
                    img_temp.flush()
                    card_variant.image.save("image.jpg", File(img_temp))
                card_variant.save()

                print(">", card_variant)
"""