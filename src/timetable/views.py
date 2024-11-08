from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet
from timetable.models import Timetable
from timetable.serializers import TimetableSerializer
from rest_framework.response import Response
from rest_framework import status

class TimetableView(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin):
    queryset = Timetable.objects.all()
    serializer_class = TimetableSerializer

    def list(self, request, *args, **kwargs):
        if 'pp' in request.GET:
            self.queryset = Timetable.objects.filter(related_timetable=request.GET['pp'])
        
        return super().list(request, *args, **kwargs)