import logging
import os

from autoslug import AutoSlugField
from django.conf import settings
from django.db import models
from django.db.models import Count
from django.utils.text import slugify
from stringcase import titlecase

logger = logging.getLogger(__name__)


def media_path():
    return settings.FILE_MEDIA_PATH


def set_logo_path(instance, filename):
    return os.path.join("sets", "{}-{}.{}".format(
        instance.slug,
        "logo",
        filename.split(".")[-1],
    ))


def set_symbol_path(instance, filename):
    return os.path.join("sets", "{}-{}.{}".format(
        instance.slug,
        "symbol",
        filename.split(".")[-1],
    ))


class Set(models.Model):
    slug = AutoSlugField(populate_from="name")
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=125)
    series = models.CharField(max_length=125)
    release_date = models.DateField(editable=True, blank=True, null=True)
    logo = models.ImageField(upload_to=set_logo_path, null=True, blank=True)
    symbol = models.ImageField(upload_to=set_symbol_path, null=True, blank=True)
    card_count = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.code})"


class Variant(models.Model):
    name = models.CharField(max_length=125)
    slug = AutoSlugField(populate_from="name", blank=True, null=True)

    def __str__(self):
        return self.name


def card_variant_image_path(instance, filename):
    return os.path.join("cards", instance.card.set.slug, "{}-{}-{}.{}".format(
        instance.card.slug,
        instance.card.number,
        instance.variant.slug,
        filename.split(".")[-1],
    ))


class CardVariant(models.Model):
    card = models.ForeignKey("Card", on_delete=models.CASCADE, related_name="variants")
    variant = models.ForeignKey(
        "Variant", on_delete=models.SET_NULL, related_name="cards", null=True
    )
    image = models.ImageField(upload_to=card_variant_image_path, null=True, blank=True)

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


def card_image_path(instance, filename):
    return os.path.join("cards", instance.set.slug, "{}-{}.{}".format(
        instance.slug,
        instance.number,
        filename.split(".")[-1],
    ))


class Card(models.Model):
    set = models.ForeignKey("Set", on_delete=models.CASCADE, related_name="cards")
    slug = AutoSlugField(populate_from="name", unique_with=["set__code"])
    name = models.CharField(max_length=125, blank=True)
    number = models.PositiveIntegerField()
    image = models.ImageField(upload_to=card_image_path, null=True, blank=True)

    supertype = models.CharField(max_length=75, blank=True, null=True)
    subtype = models.CharField(max_length=75, blank=True, null=True)
    type = models.CharField(max_length=75, blank=True, null=True)
    hp = models.PositiveIntegerField(blank=True, null=True)
    rarity = models.CharField(max_length=25, blank=True, null=True)
    illustrator = models.CharField(max_length=125, blank=True)

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
        ("3", "Good"),
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

    class Meta:
        ordering = ["-grade"]

    def __str__(self):
        return f"{self.variant}"
