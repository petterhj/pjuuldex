from django.http import Http404
from rest_framework import viewsets
from rest_framework.response import Response

from pokedex.models import Set, Card
from pokedex.serializers import SetSerializer, CardSerializer


class SetViewSet(viewsets.ModelViewSet):
    queryset = Set.objects.all()
    serializer_class = SetSerializer
    lookup_field = 'slug'


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    lookup_field = 'slug'
    
    def list(self, *args, **kwargs):
        try:
            card_set = Set.objects.get(slug=kwargs['slug'])
        except Set.DoesNotExist:
            raise Http404

        queryset = card_set.cards.all()
        serializer = CardSerializer(queryset, many=True)
        return Response(serializer.data)
