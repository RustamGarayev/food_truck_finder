from django.urls import include, path
from api import views


urlpatterns = [
    path('nearby-food-trucks', views.FoodTruckListView.as_view(), name='nearby-food-trucks'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]