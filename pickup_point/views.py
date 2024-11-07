from django.db.models import Q
from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from pickup_point.models import PickupPoint
from pickup_point.serializers import PickupPointSerializer
import csv
from datetime import date
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import action

class PickupPointView(GenericViewSet, ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin):
    queryset = PickupPoint.objects.all()
    serializer_class = PickupPointSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', None)
        
        # Get today's date
        today = date.today()

        # Filter based on search parameter
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(town__name__icontains=search) |
                Q(town__zip_code__icontains=search)
            )
        
        # Further filter the queryset to only include pickup points that are working today
        queryset = queryset.filter(
            Q(timetables__start_date__lte=today, timetables__end_date__gte=today) |
            Q(timetables__start_date__gte=today)
        ).distinct()

        return queryset

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'], url_path='json')
    def download_pickup_points(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        
        # Create a JsonResponse with the JSON data and the appropriate content type for download
        response = JsonResponse(serializer.data, safe=False)
        response['Content-Disposition'] = 'attachment; filename="pickup_points.json"'
        response['Content-Type'] = 'application/json'
        
        return response
    
    @action(detail=False, methods=['get'], url_path='csv')
    def download_pickup_points_csv(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        # Create a HttpResponse object with the appropriate CSV header
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="pickup_points.csv"'

        # Create a CSV writer
        writer = csv.writer(response)

        # Write the header row
        writer.writerow([
            'ID', 'Name', 'Observations', 'Street', 'Number', 'Floor', 
            'Latitude', 'Longitude', 'Town', 'Town Zip Code', 'Timetables'
        ])

        # Write data rows
        for pickup_point in serializer.data:
            town_name = pickup_point['town_data']['name']
            town_zip_code = pickup_point['town_data']['zip_code']
            
            # Format the timetables
            timetable_strings = []
            for timetable in pickup_point.get('timetables', []):
                start_date = timetable['start_date']
                end_date = timetable['end_date']
                times = timetable.get('times', [])
                
                # Create time string
                time_strings = []
                for time in times:
                    start_hour = time['start_hour']
                    end_hour = time['end_hour']
                    time_strings.append(f"{start_hour} - {end_hour}")
                
                # Join times with '::'
                time_string = '::'.join(time_strings)
                timetable_strings.append(f"[{start_date} - {end_date}] {time_string}")

            # Join all timetable strings with '; '
            timetable_output = '; '.join(timetable_strings)

            # Write the row for this pickup point including all required fields
            writer.writerow([
                pickup_point['id'], 
                pickup_point['name'], 
                pickup_point.get('observations', ''), 
                pickup_point.get('street', ''), 
                pickup_point.get('number', ''), 
                pickup_point.get('floor', ''), 
                pickup_point.get('latitude', ''), 
                pickup_point.get('longitude', ''), 
                town_name, 
                town_zip_code, 
                timetable_output
            ])

        return response