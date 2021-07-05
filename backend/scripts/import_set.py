import os
import argparse
import logging

os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

import django
from django.db.utils import IntegrityError
from pokemontcgsdk import Set as TCGSet

django.setup()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from scripts.util import save_image
from pokedex.models import Set#, Card, Variant, CardVariant


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-s",
        "--set",
        choices=[s.id for s in TCGSet.all()],
        required=True,
        help="Name (slug) of set to import, e.g. `base-set`",
    )
    args = parser.parse_args()
    
    tcg_set = TCGSet.find(args.set)

    logger.info("Importing set {}: {} (cards={})".format(
        tcg_set.id, tcg_set.name, tcg_set.printedTotal
    ))

    card_set = Set(
        code=tcg_set.id,
        name=tcg_set.name,
        series=tcg_set.name,
        release_date=tcg_set.releaseDate.replace("/", "-"),
        card_count=tcg_set.printedTotal,
    )

    logger.info("Saving set to database...")

    try:
        card_set.save()
        save_image(card_set.logo, tcg_set.images.logo)
        save_image(card_set.symbol, tcg_set.images.symbol)
    except IntegrityError:
        print("Could not save", card_set, "(IntegrityError)")

    logger.info("Done!")
