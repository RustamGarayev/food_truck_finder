from rest_framework import serializers

from core.models import FoodTruck


class FoodTruckSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FoodTruck
        fields = ['name', 'facility_type', 'location_description', 'address', 'latitude', 'longitude']
