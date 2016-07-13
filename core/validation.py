from rest_framework.exceptions import ParseError
def validated_period(time_period):
    """
    Validation of time period entries - conditional used here to prevent an unnecessary call to the external API.
    If successfully validated, returns the validated integer, meaning we can use it in form:
    'if validated_period(number_of days)' and for input chaining.
    :param time_period: Should be an integer between 1 and 16 days
    :return: validated time_period """
    try:
        time_period = int(time_period)
    except (TypeError, ValueError):
        raise ParseError(detail="Provided time period is not an integer between 1 and 16.")
    if time_period < 1 or time_period > 16:
        raise ParseError(detail="Provided time period is not an integer between 1 and 16.")
    return time_period


def is_city_valid(city_name):
    """
    Sanitise for emoji citynames!
    :param city_name: utf-8 encoded text string.  API will lazily match strings, so valid encoding is most important.
    :return: Raise exception or validated city name.
    """

    #specific check - hashes break the JSON encoding for the request.  Django converts back to hash from URL encoding
    if "#" in city_name:
        raise ParseError(detail="Hash characters are not allowed in City Name")
    try:
        city_name.decode('utf-8')
        return city_name
    except UnicodeError:
        raise ParseError(detail="City name contains non UTF-8 encoded characters, please check your call.")




