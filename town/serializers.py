from town.models import Town
from rest_framework.serializers import ModelSerializer

class TownSerializer(ModelSerializer):
    class Meta:
        model = Town
        fields = ('id','zip_code', 'name')
        read_only_fields = fields