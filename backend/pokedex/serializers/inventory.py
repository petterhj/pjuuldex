from rest_framework import serializers

from pokedex.models import Inventory, Card, Set
from pokedex.serializers.card import CardSerializer, CardVariantSerializer
from pokedex.serializers.set import SetSerializer


class InventoryCardSerializer(CardSerializer):
    variants = None

    class Meta:
        model = Card
        exclude = ("set",)


class InventorySerializer(serializers.ModelSerializer):
    set = SetSerializer(source="card_variant.card.set")
    card = InventoryCardSerializer(source="card_variant.card")
    variant = CardVariantSerializer(source="card_variant")
    updated_date = serializers.DateTimeField(format="%d/%m/%y")

    class Meta:
        model = Inventory
        # fields = "__all__"
        exclude = ("user", "card_variant",)
