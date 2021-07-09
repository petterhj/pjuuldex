from django.contrib import admin

from pokedex.models import (
    Set,
    Card,
    Variant,
    VariantAlias,
    CardVariant,
    Inventory,
)


@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    list_display = (
        "name", "series", "get_card_count", "get_release_year",
        "code", "slug",
    )
    readonly_fields = ("slug",)

    def get_card_count(self, obj):
        return obj.card_count
    get_card_count.short_description = "Cards"

    def get_release_year(self, obj):
        return obj.release_date.year if obj.release_date else None
    get_release_year.short_description = "Year"


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = (
        "name", "get_number", "type", "rarity", "set",
        "get_variant_count", "get_pokellector_ref", "slug",
    )
    list_filter = ("set__name",)
    readonly_fields = ("slug",)

    def get_number(self, obj):
        return obj.number
    get_number.short_description = "#"

    def get_pokellector_ref(self, obj):
        return obj.pokellector_ref
    get_pokellector_ref.short_description = 'Pokéllector'

    def get_variant_count(self, obj):
        return obj.variants.count()
    get_variant_count.short_description = "Variants"


@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ("name", "slug",)


@admin.register(VariantAlias)
class VariantAliasAdmin(admin.ModelAdmin):
    list_display = ("alias", "variant",)


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


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = (
        "user", "updated_date",
        "get_set", "get_card", 
        "get_variant", "count",
    )

    def get_set(self, obj):
        return obj.card_variant.card.set
    get_set.short_description = "Set"

    def get_card(self, obj):
        return obj.card_variant.card.name
    get_card.short_description = "Card"

    def get_variant(self, obj):
        return obj.card_variant.variant.name
    get_variant.short_description = "Variant"
