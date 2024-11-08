from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    related_pickup_point = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Report
        fields = ['id', 'related_pickup_point', 'description']
        read_only = ('id', )