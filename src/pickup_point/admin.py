from django.contrib import admin
from django.db import transaction
from .models import PickupPoint
from timetable.models import Timetable, Time  # Make sure to import your Time model

class PickupPointAdmin(admin.ModelAdmin):
    list_display = ('name', 'street', 'number', 'floor', 'town', 'latitude', 'longitude')
    search_fields = ('name', 'street', 'town__name')
    list_filter = ('town',)
    ordering = ('name',)

    def delete_model(self, request, obj):
        # Start a transaction to ensure atomicity
        with transaction.atomic():
            # Get related timetables
            related_timetables = Timetable.objects.filter(pickup_point=obj)
            # Delete associated times for each timetable
            for timetable in related_timetables:
                Time.objects.filter(timetable=timetable).delete()  # Assuming Time has a ForeignKey to Timetable
            # Now delete the related timetables
            related_timetables.delete()
            # Finally, delete the pickup point itself
            super().delete_model(request, obj)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset

admin.site.register(PickupPoint, PickupPointAdmin)