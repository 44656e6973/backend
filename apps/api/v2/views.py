from rest_framework import viewsets
from apps.core.models import Item
from .serializers import ItemV2Serializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all().order_by('-created')
    serializer_class = ItemV2Serializer
