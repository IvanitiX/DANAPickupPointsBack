from rest_framework import mixins, viewsets
from .models import Report
from .serializers import ReportSerializer

class ReportView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer