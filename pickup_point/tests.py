from django.test import TestCase
from town.models import Town  # Adjust the import based on your app structure
from .models import PickupPoint  # Adjust the import based on your app structure
from unittest.mock import patch

class PickupPointTests(TestCase):
    def setUp(self):
        # Create a town for the PickupPoint tests
        self.town = Town.objects.create(name="Test Town")

    def test_pickup_point_creation_valid(self):
        # Test creating a valid PickupPoint
        pickup_point = PickupPoint.objects.create(
            name="Test Pickup Point",
            observations="Some observations",
            street="Test Street",
            number="123",
            town=self.town
        )
        self.assertEqual(pickup_point.name, "Test Pickup Point")
        self.assertEqual(pickup_point.street, "Test Street")
        self.assertEqual(pickup_point.number, "123")
        self.assertEqual(pickup_point.town, self.town)

    @patch('geopy.geocoders.Nominatim.geocode')
    def test_get_coordinates_success(self, mock_geocode):
        # Mock the geocode method to return a location
        mock_geocode.return_value = type('Location', (object,), {'latitude': 40.7128, 'longitude': -74.0060})()

        pickup_point = PickupPoint.objects.create(
            name="Test Pickup Point",
            street="Test Street",
            number="123",
            town=self.town
        )
        pickup_point.get_coordinates()

        self.assertEqual(pickup_point.latitude, 40.7128)
        self.assertEqual(pickup_point.longitude, -74.0060)

    @patch('geopy.geocoders.Nominatim.geocode')
    def test_get_coordinates_no_result(self, mock_geocode):
        # Mock the geocode method to return None
        mock_geocode.return_value = None

        pickup_point = PickupPoint.objects.create(
            name="Test Pickup Point",
            street="Test Street",
            number="123",
            town=self.town
        )
        pickup_point.get_coordinates()

        self.assertIsNone(pickup_point.latitude)
        self.assertIsNone(pickup_point.longitude)

    @patch('geopy.geocoders.Nominatim.geocode')
    def test_save_coordinates_on_creation(self, mock_geocode):
        # Mock the geocode method to return a location
        mock_geocode.return_value = type('Location', (object,), {'latitude': 40.7128, 'longitude': -74.0060})()

        pickup_point = PickupPoint(
            name="Test Pickup Point",
            street="Test Street",
            number="123",
            town=self.town
        )
        pickup_point.save()  # This should trigger get_coordinates

        self.assertEqual(pickup_point.latitude, 40.7128)
        self.assertEqual(pickup_point.longitude, -74.0060)

    def test_pickup_point_without_coordinates(self):
        # Test creating a PickupPoint without coordinates
        pickup_point = PickupPoint.objects.create(
            name="Test Pickup Point",
            street="Test Street",
            number="123",
            town=self.town
        )
        self.assertIsNone(pickup_point.latitude)
        self.assertIsNone(pickup_point.longitude)