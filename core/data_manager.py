def make_request(city, period_in_days=3):
    """Makes request to openweather API and returns a dictionary format for parsing. Relies on time-period being
    previously validated."""

    import requests, json
    target_url = build_url(city,period_in_days)
    response = requests.get(target_url)
    return json.loads(response.text)


def build_url(city, period):
    #takes a *validated* city and period to build the request URL
    from weather.settings import APP_ID, BASE_API_URL
    parameters_string="/daily?q="+city+"&mode=json&units=metric&cnt="+str(period)+"&APPID="+APP_ID
    return BASE_API_URL+parameters_string


def create_data_list(field_name, weather_list):
    """
    :param field_name: which of the accessible elements from API we want to listify
    :param weather_list: Weather data from response.text['list']
    :return: Appropriate output list, sorted L -> H
    """
    output_list = [x[field_name] for x in weather_list]
    return output_list


def parse_data(raw_data):
    """Takes the raw data from the response and splits it into appropriate lists that we can use elsewhere, like in
    rendering a graph.  List comprehensions in main function, but would use even more repetition, so reuses function
    Design decision to use floating points rather than Decimal for the purposes of this small app.
    :param raw_data: response.text from openweather API
    :return: Dictionary containing lists of temperatures and humidity in unredacted floating points:
      """
    import numpy
    from datetime import datetime
    try:
        #the following could go straight in the dictionary, but as there are some consequential values, it makes sense
        #to declare them for reuse rather than repeating the list copmrehension to calculate the mean and modes.
        max_temps = [x['temp']['max'] for x in raw_data]
        min_temps = [x['temp']['min'] for x in raw_data]
        humidity = create_data_list("humidity", raw_data)
        daily_means = [numpy.mean(n) for n in zip(min_temps, max_temps)]
    except(KeyError, ValueError):
        raise


    dates = create_data_list("dt", raw_data)


    return {"data":
                {"temperatures": {
                    "min": max(min_temps),
                    "max": max(max_temps),
                    "mean": numpy.mean(daily_means),
                    "median": numpy.median(daily_means)},
                "humidity":{
                    "min": min(humidity),
                    "max": max(humidity),
                    "mean": numpy.mean(humidity),
                    "median": numpy.median(humidity),
                    },
                "start_date": str(datetime.fromtimestamp(min(dates)))
                }
        }


def build_graph(parsed_data):
    """
    This is a really clunky function!  Data structure chosen wasn't the best for doing the graph from, and it would be
    better refactored to use *kwargs from a more appropriate structure, as it's a one-use function as-is, and not
    particularly reusable.
    :param parsed_data:
    :return SVG rendering of graph to be incorporated into web page:
    """
    print parsed_data
    import pygal
    chart = pygal.Bar()
    chart.title = 'Weather for {city} from {date} for the next {days} days'.format(city=parsed_data['city'],
                                                                            date=parsed_data['data']['start_date'],
                                                                             days=parsed_data['number_of_days'])
    chart.x_labels = 'Min', 'Max', 'Median', 'Average'
    temperatures = parsed_data['data']['temperatures']
    humidities = parsed_data['data']['humidity']

    chart.add('Temperature', [temperatures["min"],
                            temperatures["max"],
                              temperatures["median"],
                            temperatures["mean"]])
    chart.add('Humidities', [humidities["min"],
                            humidities["max"],
                              humidities["median"],
                            humidities["mean"]], secondary=True)

    return chart.render()