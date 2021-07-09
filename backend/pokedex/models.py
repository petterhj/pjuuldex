import logging
import os

from autoslug import AutoSlugField
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

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
    pokellector_ref = models.CharField(max_length=35, unique=True, null=True, blank=False)
    name = models.CharField(max_length=125)
    series = models.CharField(max_length=125)
    release_date = models.DateField(editable=True, blank=True, null=True)
    logo = models.ImageField(upload_to=set_logo_path, null=True, blank=True)
    symbol = models.ImageField(upload_to=set_symbol_path, null=True, blank=True)
    card_count = models.PositiveIntegerField()

    class Meta:
        ordering = ["release_date", "name"]

    def __str__(self):
        return f"{self.name} ({self.code})"


class Variant(models.Model):
    name = models.CharField(max_length=125)
    slug = AutoSlugField(populate_from="name", blank=True, null=True)

    @property
    def aliases(self):
        return [va.alias for va in self.variant_aliases.all()]

    def __str__(self):
        return self.name


class VariantAlias(models.Model):
    variant = models.ForeignKey("Variant",
        on_delete=models.CASCADE,
        related_name="variant_aliases"
    )
    alias = models.CharField(max_length=125)

    def __str__(self):
        return f"{self.variant}: {self.alias}"


def card_image_path(instance, filename):
    return os.path.join("cards", instance.set.slug, "{}-{}.{}".format(
        instance.slug,
        instance.number,
        filename.split(".")[-1],
    ))


class Card(models.Model):
    set = models.ForeignKey("Set", on_delete=models.CASCADE, related_name="cards")
    slug = AutoSlugField(populate_from="name", unique_with=["set__code"])
    pokellector_ref = models.CharField(max_length=50, unique=True, null=True, blank=False)
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
    def number_id(self):
        return f"{self.number}/{self.set.card_count}"

    class Meta:
        unique_together = ["number", "set"]
        ordering = ["set", "number"]

    def __str__(self):
        return f"{self.set} - {self.name} ({self.number_id})"


def card_variant_image_path(instance, filename):
    return os.path.join("cards", instance.card.set.slug, "{}-{}-{}.{}".format(
        instance.card.slug,
        instance.card.number,
        instance.variant.slug,
        filename.split(".")[-1],
    ))


class CardVariant(models.Model):
    card = models.ForeignKey(Card,
        on_delete=models.CASCADE,
        related_name="variants"
    )
    variant = models.ForeignKey(Variant,
        on_delete=models.SET_NULL,
        related_name="cards",
        null=True,
    )
    image = models.ImageField(
        upload_to=card_variant_image_path,
        null=True,
        blank=True
    )

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


class Inventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_variant = models.ForeignKey(CardVariant, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["user", "card_variant"]
