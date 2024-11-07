from django.test import TestCase
from django.utils import timezone
from .models import Timetable, Time  # Adjust the import based on your app structure
from .serializers import TimetableSerializer  # Adjust the import based on your app structure
from rest_framework.serializers import ValidationError

class TimetableTests(TestCase):
    def setUp(self):
        # Create a valid timetable for testing
        self.valid_data = {
            'start_date': timezone.now().date() + timezone.timedelta(days=1),
            'end_date': timezone.now().date() + timezone.timedelta(days=5),
            'times': [{'start_hour': '09:00', 'end_hour': '10:00'}]
        }

    def test_timetable_creation_valid(self):
        serializer = TimetableSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        timetable = serializer.save()
        self.assertEqual(timetable.start_date, self.valid_data['start_date'])
        self.assertEqual(timetable.end_date, self.valid_data['end_date'])
        self.assertEqual(timetable.times.count(), 1)

    def test_timetable_creation_start_date_before_today(self):
        invalid_data = self.valid_data.copy()
        invalid_data['start_date'] = timezone.now().date() - timezone.timedelta(days=1)
        serializer = TimetableSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)

    def test_timetable_creation_end_date_before_today(self):
        invalid_data = self.valid_data.copy()
        invalid_data['end_date'] = timezone.now().date() - timezone.timedelta(days=1)
        serializer = TimetableSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)

    def test_timetable_creation_start_date_after_end_date(self):
        invalid_data = self.valid_data.copy()
        invalid_data['end_date'] = invalid_data['start_date'] - timezone.timedelta(days=1)
        serializer = TimetableSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)

class TimeTests(TestCase):
    def setUp(self):
        # Create a timetable for the Time model tests
        self.timetable = Timetable.objects.create(
            start_date=timezone.now().date() + timezone.timedelta(days=1),
            end_date=timezone.now().date() + timezone.timedelta(days=5)
        )
        self.valid_time_data = {
            'related_timetable': self.timetable,
            'start_hour': '09:00',
            'end_hour': '10:00'
        }

    def test_time_creation_valid(self):
        time = Time.objects.create(**self.valid_time_data)
        self.assertEqual(time.start_hour, self.valid_time_data['start_hour'])
        self.assertEqual(time.end_hour, self.valid_time_data['end_hour'])
        self.assertEqual(time.related_timetable, self.timetable)

    def test_time_creation_invalid(self):
        with self.assertRaises(ValueError):
            Time.objects.create(
                related_timetable=self.timetable,
                start_hour='10:00',
                end_hour='09:00'  # Invalid: end_hour is before start_hour
            )