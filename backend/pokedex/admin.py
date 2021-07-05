from django.contrib import admin

from pokedex.models import (
    Set,
    Card,
    Variant,
    CardVariant,
    CollectedCard,
)


@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "card_count", "slug",)
    readonly_fields = ("slug",)


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ("name", "number", "type", "rarity", "set", "slug",)
    readonly_fields = ("slug",)


@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ("name", "slug",)


@admin.register(CardVariant)
class CardVariantAdmin(admin.ModelAdmin):
    list_display = ("get_card_name", "get_card_number", "variant", "get_set_name", "has_image",)
    list_filter = ("variant__name", "card__name", "card__set__name",)
    ordering = ("card__set", "card__number",)
    
    def get_card_name(self, obj):
        return obj.card.name
    get_card_name.short_description = 'Card'

    def get_card_number(self, obj):
        return obj.card.number_id
    get_card_number.short_description = 'Number'

    def get_set_name(self, obj):
        return obj.card.set.name
    get_set_name.short_description = 'Set'

    def has_image(self, obj):
        return True if obj.image else False
    has_image.boolean = True
    has_image.short_description = 'Image'


@admin.register(CollectedCard)
class CollectedCardAdmin(admin.ModelAdmin):
    list_display = ("variant", "grade", "bought_date",)
