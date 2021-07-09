from rest_framework import serializers

from pokedex.models import Set, Card, Inventory


class SetSerializer(serializers.ModelSerializer):
    collected_count = serializers.SerializerMethodField()
    inventory_count = serializers.SerializerMethodField()

    def get_collected_count(self, obj):
        user = self.context['request'].user

        if not user.is_authenticated:
            return None

        card_ids = Inventory.objects.filter(
            user=user,
        ).values_list("card_variant__card_id").distinct()

        return Card.objects.filter(
            id__in=card_ids,
            set=obj
        ).count()

    def get_inventory_count(self, obj):
        user = self.context['request'].user

        if not user.is_authenticated:
            return None

        total_inventory_count = 0
        for collected_variant in Inventory.objects.filter(
            user=user,
            card_variant__card__in=obj.cards.all()
        ).all():
            total_inventory_count += collected_variant.count

        return total_inventory_count

    class Meta:
        model = Set
        fields = "__all__"
        lookup_field = "slug"


class SetDetailSerializer(SetSerializer):
    from pokedex.serializers.card import CardSerializer

    cards = CardSerializer(many=True)
