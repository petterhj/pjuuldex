from rest_framework import serializers

from pokedex.models import Set, Card, CardVariant, CollectedCard


class SetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Set
        fields = "__all__"
        lookup_field = "slug"
        read_only_fields = ("slug",)


class CollectedCardSerializer(serializers.ModelSerializer):
    grade = serializers.CharField(source='get_grade_display')

    class Meta:
        model = CollectedCard
        fields = ("id", "grade", "bought_date",)


class CardVariantSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='variant.name')
    inventory = CollectedCardSerializer(read_only=True, many=True)

    class Meta:
        model = CardVariant
        fields = ("id", "name", "image", "inventory",)


class CardSerializer(serializers.ModelSerializer):
    set = SetSerializer()
    variants = CardVariantSerializer(many=True)
    # image = serializers.CharField()
    # type = serializers.CharField(source='get_type_display')
    # stage = serializers.CharField(source='get_stage_display')
    # color = serializers.CharField(source='get_color_display')
    # rarity = serializers.CharField(source='get_rarity_display')
    inventory_count = serializers.IntegerField()

    class Meta:
        model = Card
        fields = "__all__"
        lookup_field = "slug"
        read_only_fields = ("slug",)
