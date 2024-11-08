from django.contrib import admin
from .models import Report

class ReportAdmin(admin.ModelAdmin):
    list_display = ('related_pickup_point', 'description')  # Assuming you have a created_at field
    search_fields = ('description',)
    list_filter = ('related_pickup_point',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Optionally, you can annotate or modify the queryset here
        return queryset

admin.site.register(Report, ReportAdmin)