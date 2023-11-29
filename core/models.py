from django.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.db import models as gis_models


FACILITY_TYPE = (
    ('T', 'Truck'),
    ('P', 'Push Cart'),
)


class FoodTruck(models.Model):
    """
    Note: Below fields are not the only fields in the CSV file,
          but they are the only ones we care about for this project
    """

    name = models.CharField(max_length=255)
    facility_type = models.CharField(choices=FACILITY_TYPE, max_length=3, default='N/A')
    location_description = models.TextField()
    address = models.CharField(max_length=500)
    latitude = models.FloatField()
    longitude = models.FloatField()
    point_location = gis_models.PointField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Override save method to create PointField from latitude and longitude
        """
        self.point_location = Point(self.longitude, self.latitude)
        super(FoodTruck, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
