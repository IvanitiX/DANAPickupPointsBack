from rest_framework.serializers import ModelSerializer, ValidationError, SerializerMethodField, CharField

from pickup_point.models import PickupPoint
from timetable.models import Timetable, Time
from timetable.serializers import TimetableSerializer
from town.serializers import TownSerializer

class PickupPointSerializer(ModelSerializer):
    timetables = TimetableSerializer('timetables', many=True, required=False)
    town_data = SerializerMethodField()
    number = CharField(required=False, allow_blank=True)
    floor = CharField(required=False, allow_blank=True)
    observations = CharField(required=False, allow_blank=True)

    def get_town_data(self, obj):
        return TownSerializer(obj.town).data

    def create(self, validated_data):
        if 'number' not in validated_data:
            validated_data['number'] = 's/n'
            
        timetables = validated_data.pop('timetables')
        
        pickup_point = PickupPoint.objects.create(**validated_data)
        for timetable in timetables:
            times = None

            if 'times' in timetable:
                times = timetable.pop('times')

            new_tt = Timetable.objects.create(related_pickup_point=pickup_point, **timetable)

            if times:
                for time in times:
                    Time.objects.create(related_timetable=new_tt, **time)

        return pickup_point

    class Meta:
        model = PickupPoint
        fields = (
            'id',
            'name',
            'observations',
            'street',
            'number',
            'floor',
            'latitude',
            'longitude',
            'town',
            'town_data',
            'timetables',
        )

        read_only_fields = ('id','town_data','latitude','longitude')