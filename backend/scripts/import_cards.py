import os
import argparse
from urllib.request import urlopen
from tempfile import NamedTemporaryFile

os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

import django
from django.core.files import File
from django.db.utils import IntegrityError

django.setup()

from pokedex.models import Set, Card, Variant, CardVariant
from lib.pkmncards import search_card


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
    parser.add_argument(
        "-n",
        "--card-number",
        required=False,
        help="Import specified card only",
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
