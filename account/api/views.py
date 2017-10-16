from rest_framework.decorators import api_view
from rest_framework.response import Response
from account.models import Country, City
from account.api.serializers import CountrySerializer, CitySerializer


@api_view(['GET'])
def countries(request):
    """
    get all countries   
    """
    if request.method == 'GET':
        countries = Country.objects.all()
        serialized = CountrySerializer(list(countries), many=True) # serializers.serialize('json', countries)
        return Response(serialized.data)


@api_view(['GET'])
def cities_by_country(request, country_id):
    """
    get all cities by country     
    """
    if request.method == 'GET':
        cities = City.objects.filter(country__exact=country_id)
        serialized = CitySerializer(list(cities), many=True)
       # cities = geonames.cities_by_country_list(country_id) #Country.objects.all()
        return Response(serialized.data)
