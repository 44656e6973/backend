from rest_framework import serializers
from apps.core.models import Item

class ItemV2Serializer(serializers.ModelSerializer):
    api_version = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'created', 'api_version']

    def get_api_version(self, obj):
        return 'v2'
