from rest_framework import serializers

from pokedex.models import Card, CardVariant, Inventory


class CardVariantSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='variant.name')
    aliases = serializers.ListField(source='variant.aliases')
    inventory_count = serializers.SerializerMethodField()

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if instance.image:
            response["image"] = instance.image.url
        return response

    def get_inventory_count(self, obj):
        user = self.context['request'].user

        if not user.is_authenticated:
            return None

        inventory = Inventory.objects.filter(
            user=user,
            card_variant=obj,
        ).first()

        return inventory.count if inventory else 0

    class Meta:
        model = CardVariant
        # fields = ("id", "name", "aliases",)
        fields = "__all__"


class CardSerializer(serializers.ModelSerializer):
    variants = CardVariantSerializer(many=True)
    inventory_count = serializers.SerializerMethodField()

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if instance.image:
            response["image"] = instance.image.url
        return response

    def get_inventory_count(self, obj):
        user = self.context['request'].user

        if not user.is_authenticated:
            return None

        total_count = 0
        for variant in Inventory.objects.filter(
            user=user,
            card_variant__card=obj,
        ).all():
            total_count += variant.count
        return total_count
    
    class Meta:
        model = Card
        fields = "__all__"
        lookup_field = "slug"


class CardDetailSerializer(CardSerializer):
    from pokedex.serializers.set import SetSerializer

    set = SetSerializer()
