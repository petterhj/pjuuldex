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

import lib.pokellector as pokellector
from pokedex.utils import get_or_none, save_image
from pokedex.models import Set, Card, Variant, CardVariant


def import_set(tcg_set, pokellector_ref) -> Set:
    card_set = get_or_none(Set, code=tcg_set.id)

    if card_set:
        logger.info(f"Set {card_set} already exists (skipping)")
        
        if not card_set.pokellector_ref:
            logger.info(f"Updating Pokellector ref for set ({pokellector_ref})")
            card_set.pokellector_ref = pokellector_ref
            card_set.save()

        return card_set

    logger.info("Importing set {}: {} (cards={})".format(
        tcg_set.id, tcg_set.name, tcg_set.printedTotal
    ))

    card_set = Set(
        code=tcg_set.id,
        pokellector_ref=pokellector_ref,
        name=tcg_set.name,
        series=tcg_set.name,
        release_date=tcg_set.releaseDate.replace("/", "-"),
        card_count=tcg_set.printedTotal,
    )

    logger.info("Saving set to database...")

    card_set.save()
    save_image(card_set.logo, tcg_set.images.logo)
    save_image(card_set.symbol, tcg_set.images.symbol)

    logger.info("Done importing set data!")

    return card_set


def import_card(card_set, tcg_card, pokellector_ref) -> Card:
    logger.info(f"Importing card #{tcg_card.number}: {tcg_card.name}...")

    card = get_or_none(Card, set=card_set, number=int(tcg_card.number))
    
    if card:
        logger.info(f"Card {card} already exists (skipping)")

        if not card.pokellector_ref:
            logger.info(f"Updating Pokellector ref for card ({pokellector_ref})")
            card.pokellector_ref = pokellector_ref
            card.save()

        return card

    card = Card(
        set=card_set,
        pokellector_ref=pokellector_ref,
        name=tcg_card.name,
        number=int(tcg_card.number),
        supertype=tcg_card.supertype,
        subtype=",".join(tcg_card.subtypes) if tcg_card.subtypes else None,
        type=",".join(tcg_card.types) if tcg_card.types else None,
        hp=tcg_card.hp,
        rarity=tcg_card.rarity,
        illustrator=tcg_card.artist,
    )

    logger.info(f"Saving card #{card.number}: {card.name} to database...")

    card.save()
    save_image(card.image, tcg_card.images.small)

    return card


def update_variants(card, pokellector_variants):
    logger.info(f"Updating variants for {card}: {', '.join(pokellector_variants)}")

    for variant in ["Unlimited"] + pokellector_variants:
        variant, created_variant = Variant.objects.get_or_create(
            name=variant
        )

        if created_variant:
            logger.info(f"Created variant {variant}")

        card_variant, created_card_variant = CardVariant.objects.get_or_create(
            card=card,
            variant=variant
        )

        if created_card_variant:
            logger.info(f"Created card variant {card_variant}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-s",
        "--set",
        choices=[s.id for s in TCGSet.all()],
        required=True,
        help="Name (slug) of set to import, e.g. `base1`",
    )
    parser.add_argument(
        "-p",
        "--pokellector-ref",
        required=True,
        help="Pokéllector reference ID",
    )
    parser.add_argument(
        "-n",
        "--card-number",
        required=False,
        help="Import specified card(s) only (comma separated)",
    )
    args = parser.parse_args()

    tcg_set = TCGSet.find(args.set)
    pokellector_set = pokellector.get_cards(args.pokellector_ref)

    if tcg_set.printedTotal != len(pokellector_set):
        raise Exception("Set card count mismatch: tcg={}, pokellector={}!".format(
            tcg_set.printedTotal, len(pokellector_set)
        ))

    card_set = import_set(tcg_set, args.pokellector_ref)
    card_numbers = [int(cn) for cn in args.card_number.split(",")] if args.card_number else []
    
    if not card_numbers:
        tcg_cards = TCGCard.where(q=f"set.id:{card_set.code}")
    else:
        tcg_cards = [TCGCard.find(f"{card_set.code}-{cn}") for cn in card_numbers]

    logger.info("Importing {} card(s) from {}: {} (total={})".format(
        len(tcg_cards), card_set.code, card_set.name, card_set.card_count
    ))

    for tcg_card in tcg_cards:
        pokellector_ref = pokellector_set[int(tcg_card.number)]
        card = import_card(card_set, tcg_card, pokellector_ref)

        pokellector_variants = pokellector.get_variants(pokellector_ref)
        if pokellector_variants:
            update_variants(card, pokellector_variants)

