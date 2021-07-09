from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from pokedex.models import (
    Set,
    Card,
    CardVariant,
    Inventory,
)
from pokedex.serializers.set import (
    SetSerializer,
    SetDetailSerializer,
)
from pokedex.serializers.card import (
    CardDetailSerializer,
)
from pokedex.serializers.inventory import (
    InventorySerializer,
)


class SetViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Set.objects.all()
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SetDetailSerializer
        return SetSerializer


class CardViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = "slug"

    def get_queryset(self):
        return Card.objects.filter(
            set__slug=self.kwargs["set_slug"]
        )

    def get_serializer_class(self):
        return CardDetailSerializer
    

class InventoryViewSet(viewsets.ModelViewSet):
    serializer_class = InventorySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Inventory.objects.filter(
            user=self.request.user
        ).order_by("-updated_date")

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = get_object_or_404(queryset,
            card_variant__pk=self.kwargs["variant_pk"]
        )
        self.check_object_permissions(self.request, obj)
        return obj

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()[0:5]
        serialized = self.get_serializer(queryset, many=True)
        return Response(serialized.data)

    def create(self, request, variant_pk, **kwargs):
        card_variant = get_object_or_404(
            CardVariant,
            pk=variant_pk
        )
        
        inventory, created = Inventory.objects.get_or_create(
            user=request.user,
            card_variant=card_variant,
        )

        inventory.count += 1
        inventory.save()

        serializer = self.get_serializer(inventory)
        return Response(serializer.data)

    def destroy(self, request, variant_pk, **kwargs):
        inventory = self.get_object()
        
        if inventory.count > 1:
            inventory.count -= 1
            inventory.save()
        elif inventory.count == 1:
            inventory.count = 0
            inventory.delete()

        serialized = self.get_serializer(inventory)
        return Response(serialized.data)
