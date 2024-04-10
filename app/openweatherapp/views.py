from django.shortcuts import render
import requests
from .models import City
import datetime
import math
from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from django.views import View
#forms
from .forms import CityForm

from .serializer import (
    Citieserializer
)


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=605722ecd79962b1dd142ca55dada0dc'

    cities = City.objects.all() 

    if request.method == 'POST': 
        form = CityForm(request.POST) 
        form.save()
    
    form = CityForm()
    data = []

    for city in cities:
        city_weather = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types
        weather = {
            'city' : city,
            'temperature' : city_weather['main']['temp'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon']
        }
        data.append(weather) #add the data for the current city into our list

    context = {'data' : data, 'form' : form}
    return render(request, 'openweatherapp/index.html', context) #returns the index.html template


# Cities Generic View
class Cities(generics.GenericAPIView):
    serializer_class = Citieserializer
    queryset =City.objects.all()
    assert queryset.ordered == False

    def get(self, request):
        page_num = int(request.GET.get("page", 1))
        limit_num = int(request.GET.get("limit", 10))
        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num
        search_param = request.GET.get("search")
        cities = City.objects.all()
        total_cities = cities.count()
        if search_param:
            cities = cities.filter(title__icontains=search_param)
        serializer = self.serializer_class(cities[start_num:end_num], many=True)
        return Response({
            "status": "success",
            "total": total_cities,
            "page": page_num,
            "last_page": math.ceil(total_cities / limit_num),
            "notes": serializer.data
        })

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": {"note": serializer.data}}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        



# Cities Details
class CityDetail(generics.GenericAPIView):
    queryset = City.objects.all()
    serializer_class = Citieserializer

    def get_note(self, pk):
        try:
            return City.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        cities = self.get_note(pk=pk)
        if cities == None:
            return Response({"status": "fail", "message": f"Note with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(cities)
        return Response({"status": "success", "data": {"note": serializer.data}})

    def patch(self, request, pk):
        cities = self.get_note(pk)
        if cities == None:
            return Response({"status": "fail", "message": f"Note with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            cities, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.validated_data['updatedAt'] = datetime.now()
            serializer.save()
            return Response({"status": "success", "data": {"note": serializer.data}})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        cities = self.get_note(pk)
        if cities == None:
            return Response({"status": "fail", "message": f"Note with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        cities.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Viewset
class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = Citieserializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.active = False
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)      



