from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ParseError

@api_view(['GET'])
def weather_endpoint(request, city, period_in_days=3):
    """
    Main endpoint for weather response.\n
    :param request: request object from browser\n
    :param city: City object, URL encoded - hashes will result in Parse error.\n
    :param period_in_days: Integer in range 1-16\n
    :return: JSON response - Temperature and Humidity for next X days broken in Min, Max, Median, Mean
    """
    from validation import validated_period, is_city_valid
    from data_manager import parse_data, make_request
    try:
        city = is_city_valid(city)
        period_in_days=validated_period(period_in_days)
        response = make_request(city, period_in_days)
    except ParseError, e:
        return Response({"detail":e.detail}, status=status.HTTP_400_BAD_REQUEST)

    #strip out weather data from other details.
    raw_weather_data = response['list']

    try:
        full_response = {"city":response['city']['name'],
                        "number_of_days":period_in_days,
                        "data": parse_data(raw_weather_data)}

        return Response(full_response, status=status.HTTP_200_OK)
    except(KeyError, ValueError):
        return Response(
                {"Detail": "Sorry, something unexpected happened, please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                        )

@api_view(['GET'])
def graph_endpoint(request, city, period_in_days=3):
    """
    Additional endpoint to render graph for weather response.  Returns JSON response of .svg, which can be embedded on
    user's page, rather than being served from our servers. \n
    Certain amount of repetition - would move the core 'build response' info into its own function after this -
     just to show proof of concept.\n

    :param request: request object from browser\n
    :param city: City object, URL encoded - hashes will result in Parse error.\n
    :param period_in_days: Integer in range 1-16\n
    :return: SVG data
    """
    from validation import validated_period, is_city_valid
    from data_manager import parse_data, make_request, build_graph
    try:
        city = is_city_valid(city)
        period_in_days=validated_period(period_in_days)
        response = make_request(city, period_in_days)
    except ParseError, e:
        return Response({"detail":e.detail}, status=status.HTTP_400_BAD_REQUEST)

    #strip out weather data from other details.
    raw_weather_data = response['list']

    full_response = {"city":response['city']['name'],
                    "number_of_days":period_in_days,
                    "data": parse_data(raw_weather_data)['data']}
    graph = build_graph(full_response)
    print graph
    return Response({"graph":graph}, status=status.HTTP_200_OK)


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
