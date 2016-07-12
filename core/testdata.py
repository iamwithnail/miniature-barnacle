"""Some of the longer data options for testing are placed here for readibility/replaceability.  Ideally these would be
positioned as fixtures, alongside database data."""
import datetime
correct_url = "http://api.openweathermap.org/data/2.5/forecast/daily?q=London&mode=json&units=metric&cnt=3&APPID=cea6b91ccc5f25041e7e094ef85787fe"

sample_data = [{
u'clouds': 56,
    u'temp': {
        u'min': 10.13,
        u'max': 17.03,
        u'eve': 14.47,
        u'morn': 16.65,
        u'night': 10.13,
        u'day': 16.65
    },
    u'rain': 3.4,
    u'humidity': 79,
    u'pressure': 1017.81,
    u'weather': [{
        u'main': u'Rain',
        u'id': 501,
        u'icon': u'10d',
        u'description': u'moderate rain'
    }],
    u'dt': 1468324800,
    u'speed': 4.76,
    u'deg': 282
}, {
    u'clouds': 92,
    u'temp': {
        u'min': 10.97,
        u'max': 17.17,
        u'eve': 16.25,
        u'morn': 10.97,
        u'night': 12.34,
        u'day': 16.35
    },
    u'humidity': 76,
    u'pressure': 1024.67,
    u'weather': [{
        u'main': u'Rain',
        u'id': 500,
        u'icon': u'10d',
        u'description': u'light rain'
    }],
    u'dt': 1468411200,
    u'speed': 5.83,
    u'deg': 312
}, {
    u'clouds': 36,
    u'temp': {
        u'min': 12.07,
        u'max': 18.39,
        u'eve': 17.78,
        u'morn': 12.07,
        u'night': 12.83,
        u'day': 17.16
    },
    u'humidity': 79,
    u'pressure': 1030.08,
    u'weather': [{
        u'main': u'Clouds',
        u'id': 802,
        u'icon': u'03d',
        u'description': u'scattered clouds'
    }],
    u'dt': 1468497600,
    u'speed': 3.91,
    u'deg': 329
}]

response_to_test_data = {'data':
                             {'start_date': '2016-07-12 12:00:00',
                              'temperatures': {'max': 18.39,
                                               'mean': 14.293333333333335,
                                               'median': 14.07,
                                               'min': 12.07},
                              'humidity': {'max': 79,
                                           'mean': 78.0,
                                           'median': 79.0,
                                           'min': 76}}}
