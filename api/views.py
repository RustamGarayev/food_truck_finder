from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from core.models import FoodTruck
from api.serializers import FoodTruckSerializer
from api.helpers import is_valid_ip, is_valid_lat_long, get_location_from_ip

from django.db.models import QuerySet
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError

from django.contrib.gis.db.models.functions import Distance


class FoodTruckListView(APIView):
    """
    API endpoint that allows food trucks to be viewed or edited.
    """

    queryset = FoodTruck.objects.all().order_by("-created_at")
    serializer_class = FoodTruckSerializer
    permission_classes = [
        permissions.AllowAny
    ]  # TODO: change to IsAuthenticated/IsAdminUser for production

    @staticmethod
    def get_manual_parameters():
        return [
            openapi.Parameter(
                name="current_address",
                in_=openapi.IN_QUERY,
                description="Either IP address or Lat/Long separated by comma",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                name="number_of_trucks",
                in_=openapi.IN_QUERY,
                description="Limiting number for the returned response",
                type=openapi.TYPE_INTEGER,
                default=5,
            ),
        ]

    @staticmethod
    def _find_nearby_food_trucks(
        latitude: float, longitude: float, number_of_food_trucks: int
    ) -> QuerySet[FoodTruck]:
        """
        Using Geographic Database Functions to order nearby food trucks by distance and return the top n results
        Reference: https://docs.djangoproject.com/en/4.2/ref/contrib/gis/functions/#distance
        """
        user_location = Point(longitude, latitude, srid=4326)
        nearby_trucks = FoodTruck.objects.annotate(
            distance=Distance("point_location", user_location)
        ).order_by("distance")[:number_of_food_trucks]

        return nearby_trucks

    @staticmethod
    def _get_client_ip(request):
        # Ref: https://stackoverflow.com/a/4581997/11923558
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip

    @swagger_auto_schema(manual_parameters=get_manual_parameters())
    def get(self, request):
        """
        This view will return a list of certain number of nearby food trucks based on the user's IP address.
        If the IP address is not provided, it will use the user's current IP address.
        If the IP address is invalid, it will return a 400 error.
        """
        current_user_ip = self._get_client_ip(self.request)

        # Allow user to pass in IP address to test from different locations
        filter_address = request.GET.get("current_address", current_user_ip).strip()

        number_of_trucks = request.GET.get("number_of_trucks", 5)

        try:
            latitude, longitude = None, None

            if is_valid_ip(filter_address):
                latitude, longitude = get_location_from_ip(filter_address)
            elif "," in filter_address and len(filter_address.split(",")) == 2:
                lat_str, lng_str = filter_address.split(",")
                if is_valid_lat_long(lat_str, lng_str):
                    latitude, longitude = float(lat_str), float(lng_str)
                else:
                    raise ValidationError("Invalid latitude/longitude format.")

            if latitude is None or longitude is None:
                raise ValidationError(
                    "Invalid input format. Provide an IP address or latitude,longitude pair."
                )

            # If everything is valid, return the nearby food trucks based on the latitude/longitude
            nearby_food_trucks = self._find_nearby_food_trucks(
                latitude, longitude, int(number_of_trucks)
            )

            serializer = FoodTruckSerializer(nearby_food_trucks, many=True)
            return Response(serializer.data, status=200)
        except ValidationError as e:
            return Response({"error": str(e)}, status=400)
