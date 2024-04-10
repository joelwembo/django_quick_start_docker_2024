from django.contrib import admin
from django.urls import path , include , re_path
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


# Utils and Libraries
# Swagger API Docs
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

user_list = CityViewSet.as_view({'get': 'list'})
user_detail = CityViewSet.as_view({'get': 'retrieve'})

urlpatterns = router.urls


schema_view = get_schema_view(
    openapi.Info(
        title="Weather API",
        default_version='v1',
        description="API services built by Joel Otepa Wembo",
        terms_of_service="https://domain.io/policies/terms/",
        contact=openapi.Contact(email="me@joelwembo.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('openweatherapp.urls')),
    path('api/v1/weather/', include(cities_urls)),
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger',
            cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc',
            cache_timeout=0), name='schema-redoc'),   
]

urlpatterns += router.urls
