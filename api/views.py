from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from core.models import FoodTruck
from api.serializers import FoodTruckSerializer

from django.contrib.gis.geos import Point
from django.contrib.gis.geoip2 import GeoIP2
from geoip2.errors import AddressNotFoundError

from django.contrib.gis.db.models.functions import Distance


class FoodTruckListView(APIView):
    """
    API endpoint that allows food trucks to be viewed or edited.
    """
    queryset = FoodTruck.objects.all().order_by('-created_at')
    serializer_class = FoodTruckSerializer
    permission_classes = [permissions.AllowAny]  # TODO: change to IsAuthenticated/IsAdminUser for production

    @staticmethod
    def _get_location_from_ip(ip_address: str) -> (float, float):
        geo_ip = GeoIP2()
        lat, lng = geo_ip.lat_lon(ip_address)
        return lat, lng

    @staticmethod
    def _find_nearby_food_trucks(latitude: float, longitude: float, number_of_food_trucks: int):
        """
        Using Geographic Database Functions to order nearby food trucks by distance and return the top n results
        Reference: https://docs.djangoproject.com/en/4.2/ref/contrib/gis/functions/#distance
        """
        user_location = Point(longitude, latitude, srid=4326)
        nearby_trucks = FoodTruck.objects.annotate(
            distance=Distance('point_location', user_location)
        ).order_by('distance')[:number_of_food_trucks]

        return nearby_trucks

    @staticmethod
    def _get_client_ip(request):
        # Ref: https://stackoverflow.com/a/4581997/11923558
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get(self, request):
        """
        This view should return a list of certain number of nearby food trucks
        ip_address -- IP address against which the location is determined
        number_of_trucks -- Limiting number for the returned response
        """
        current_user_ip = self._get_client_ip(self.request)
        # print(current_user_ip)
        # print("************")

        # Allow user to pass in IP address to test from different locations
        filter_ip = request.GET.get('ip_address', current_user_ip).strip()

        number_of_trucks = request.GET.get('number_of_trucks', 5)

        try:
            # Get user's lat/lgt values from the IP address
            latitude, longitude = self._get_location_from_ip(filter_ip)

            # Get nearby food trucks
            nearby_food_trucks = self._find_nearby_food_trucks(latitude, longitude, int(number_of_trucks))

            # Serialize the data
            serializer = FoodTruckSerializer(nearby_food_trucks, many=True)

            return Response(serializer.data)
        except AddressNotFoundError:
            return Response(FoodTruck.objects.none())
