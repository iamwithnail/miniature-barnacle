from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ParseError




from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser





@api_view(['GET'])
def weather_endpoint(request, city, period_in_days=3):
    from validation import  make_request, parse_data
    try:
        response = make_request(city, period_in_days)
    except ParseError, e:
        return Response({"detail": e}, status=status.HTTP_400_BAD_REQUEST)

    #strip out weather data from other details.
    raw_weather_data = response['list']

    full_response = {"city":response['city']['name'],
                    "number_of_days":period_in_days,
                    "data": parse_data(raw_weather_data)}

    return Response(full_response, status=status.HTTP_200_OK)

@api_view(['GET'])
def render_graph(request, city, period_in_days=3):
    from validation import build_graph

    graph_data = build_graph(parsed_data)
