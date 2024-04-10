from django.contrib import admin
from django.urls import path , include
from take_home import views
from django.views import generic
# Django Rest Framework
from rest_framework import routers, permissions , views, serializers, status
from rest_framework.response import Response
from rest_framework.schemas import get_schema_view
# Apps
from openweatherapp import urls as cities_urls
# viewset
from openweatherapp.views import CityViewSet
# graphQL
from openweatherapp.schema import schema
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt

# router for viewset API
router = routers.DefaultRouter()
router.register(r'router/weather', CityViewSet, basename="cities")


user_list = CityViewSet.as_view({'get': 'list'})
user_detail = CityViewSet.as_view({'get': 'retrieve'})

urlpatterns = router.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('openweatherapp.urls')),
    path('api/v1/weather/', include(cities_urls)),
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]

urlpatterns += router.urls
