from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ParseError

@api_view(['GET'])
def weather_endpoint(request, city, period_in_days=3):
    print "DEBUG ENDPOINT", period_in_days, type(period_in_days)
    from validation import make_request, parse_data, validated_period
    try:
        response = make_request(city, validated_period(period_in_days))
    except ParseError, e:
        return Response({"detail":e.detail}, status=status.HTTP_400_BAD_REQUEST)

    #strip out weather data from other details.
    raw_weather_data = response['list']

    full_response = {"city":response['city']['name'],
                    "number_of_days":period_in_days,
                    "data": parse_data(raw_weather_data)}

    return Response(full_response, status=status.HTTP_200_OK)

@api_view(['GET'])
def page_not_found(request):
    content = {"detail": 'The endpoint you have requested has not been found.  Navigate to the root URL and use OPTIONS'}
    return Response(content, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'OPTIONS'])
def root(request):
    if request.method=='GET':
        content = {"detail": "URL working as expected. Use OPTIONS to see a list of endpoints and service description"}
        return Response(content, status=status.HTTP_200_OK)
    elif request.method=='OPTIONS':
        content = {"description":  "Uses open weather API to provide mean, median, max and minimum temperatures and humidity for the next X days",
                   "format": "/{city}/{number_of_days} - number of days should be between 1 and 16",
                   "methods": "GET allowed to weather endpoint, other methods will be refused.  OPTIONS allowed on root"
                   }
        return Response(content, status=status.HTTP_200_OK)
