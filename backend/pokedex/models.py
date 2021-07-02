import os
import logging

from autoslug import AutoSlugField
from django.conf import settings
from django.db import models
from django.db.models import Count
from stringcase import titlecase


logger = logging.getLogger(__name__)


def media_path():
    return settings.FILE_MEDIA_PATH


class Set(models.Model):
    slug = AutoSlugField(populate_from="name")
    name = models.CharField(max_length=125)
    code = models.CharField(max_length=5, unique=True)
    card_count = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.code})"


def card_image_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "{}-{}-{}.{}".format(
        instance.card.slug,
        instance.card.number,
        instance.variant.slug,
        ext,
    )
    return os.path.join("cards", instance.card.set.slug, filename)


class Variant(models.Model):
    name = models.CharField(max_length=125)
    slug = AutoSlugField(populate_from="name", blank=True, null=True)

    def __str__(self):
        return self.name


class CardVariant(models.Model):
    card = models.ForeignKey("Card", on_delete=models.CASCADE, related_name="variants")
    variant = models.ForeignKey(
        "Variant", on_delete=models.SET_NULL, related_name="cards", null=True
    )
    image = models.ImageField(upload_to=card_image_path, null=True, blank=True)

    class Meta:
        unique_together = ["card", "variant"]
        ordering = ["variant__name"]

    def __str__(self):
        return "{}: {} ({}, {})".format(
            self.card.set.name,
            self.card.name,
            self.card.number_id,
            self.variant.name,
        )


class Card(models.Model):
    TYPES = ((t, titlecase(t)) for t in [
        "pokemon", "trainer", "supporter", "item", "energy",
        # "pokemon-tool", "stadium", "special-energy",
        # "basic-energy", "technical-machine", "rockets-secret-machine",
        # "pokemon-tool-f", "goldenrod-game-corner",
    ])
    STAGES = ((s, titlecase(s)) for s in [
        "basic", "stage-1", "stage-2",
        # vmax, mega, level-up, break,
        # baby, legend, restored
    ])
    COLORS = ((c, c.capitalize()) for c in [
        "grass", "water", "fire", "lightning",
        "psychic", "fighting", "colorless",
        # "fairy", "dragon", "darkness", "metal",
    ])
    RARITY = ((r, titlecase(r)) for r in [
        "common", "uncommon", "rare", "rare-holo",
        # promo, rare-ultra, rare-secret, rare-rainbow,
        # rare-holo-uppercase-ex, rare-holo-gx, rare-shiny,
        # rare-holo-lowercase-ex, rare-holo-v, rare-holo-lv-x,
        # rare-holo-vmax, rare-shiny-gx, rare-break, rare-prism-star,
        # rare-prime, rare-holo-star, legend, rare-shining, rare-ace,
        # amazing-rare, rare-shiny-v, rare-shiny-vmax
    ])

    set = models.ForeignKey("Set", on_delete=models.CASCADE, related_name="cards")
    slug = AutoSlugField(populate_from="name", unique_with=["set__code"])
    name = models.CharField(max_length=125, blank=True)
    number = models.PositiveIntegerField()

    type = models.CharField(max_length=25, choices=TYPES, blank=True, null=True)
    stage = models.CharField(max_length=10, choices=STAGES, blank=True, null=True)
    color = models.CharField(max_length=10, choices=COLORS, blank=True, null=True)
    rarity = models.CharField(max_length=25, choices=RARITY, blank=True, null=True)
    hp = models.PositiveIntegerField(blank=True, null=True)
    illustrator = models.CharField(max_length=125, blank=True)

    @property
    def image(self):
        for variant in self.variants.annotate(
            inventory_count=Count("inventory")
        ).order_by("-inventory_count"):
            if variant.image:
                return variant.image.url
        return None

    @property
    def inventory_count(self):
        inventory_count = 0
        for variant in self.variants.annotate(
            inventory_count=Count("inventory")
        ).order_by("-inventory_count"):
            inventory_count += variant.inventory_count
        return inventory_count

    @property
    def number_id(self):
        return f"{self.number}/{self.set.card_count}"

    class Meta:
        unique_together = ["number", "set"]
        ordering = ["number"]

    def __str__(self):
        return f"{self.set} - {self.name} ({self.number_id})"


class CollectedCard(models.Model):
    GRADES = (
        ("1", "Poor"),
        ("2", "OK"),
        ("2", "Good"),
        ("4", "Excellent"),
    )

    variant = models.ForeignKey(
        "CardVariant",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="inventory",
    )
    grade = models.CharField(
        max_length=1, choices=GRADES, blank=True, null=True
    )
    bought_date = models.DateField(editable=True, blank=True, null=True)

    def __str__(self):
        return f"{self.variant}"
