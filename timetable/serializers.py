from timetable.models import Timetable, Time
from datetime import time
from datetime import date
from rest_framework.serializers import ModelSerializer, ValidationError

class TimeSerializer(ModelSerializer):

    def validate(self, attrs):
        print(attrs)
        start_hour = attrs.get('start_hour')
        end_hour = attrs.get('end_hour')
        open_all_day = attrs.get('open_all_day')

        if start_hour and end_hour and end_hour < start_hour:
            raise ValidationError("La hora de inicio debe ser antes de la hora de fin")
        
        if open_all_day and open_all_day == True:
            attrs['start_hour'] = time(hour=0,minute=0)
            attrs['end_hour'] = time(hour=23,minute=59)
        
        return attrs
        
    class Meta:
        model = Time
        fields = ('start_hour', "end_hour", "open_all_day")

class TimetableSerializer(ModelSerializer):
    times = TimeSerializer('times',many=True)

    def validate(self, attrs):
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')

        # Check if both dates are not before today
        if start_date < date.today() or end_date < date.today():
            raise ValidationError("Las fechas no pueden ser anteriores a hoy.")

        # Check if start_date is greater than end_date
        if start_date > end_date:
            raise ValidationError("La fecha de inicio debe ser antes de la fecha de fin.")

        return attrs

    def create(self, validated_data):
        times = validated_data.pop('times')
        timetable = Timetable.objects.create(**validated_data)
        for time in times:
            Time.objects.create(related_timetable=timetable, **time)

        return timetable

    class Meta:
        model = Timetable
        fields = ('start_date','end_date','times')