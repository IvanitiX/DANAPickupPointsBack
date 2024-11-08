from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from town.models import Town
from town.serializers import TownSerializer

class TownListView(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = Town.objects.all()
    serializer_class = TownSerializer

    def list(self, request, *args, **kwargs):
        if 'codp' in request.GET:
            self.queryset = Town.objects.filter(zip_code=request.GET['codp'])
        elif 'loc' in request.GET:
            self.queryset = Town.objects.filter(name__icontains=request.GET['loc'])
        
        return super().list(request, *args, **kwargs)