# miniature-barnacle

**Installation** 

Note: If installing on a *nix system, you may need to install the development versions of two libraries - the build below will fail with the message 

```
make sure the development packages of libxml2 and libxslt are installed * 
``` 
at the requirements.txt stage.   If that happens, run 
``` 
sudo apt-get install python-dev libxml2-dev libxslt1-dev zlib1g-dev 
```
These libraries support Pygal & Numpy.  Otherwise, run: 

```
    Virtualenv env
    source env/bin/activate
    git clone https://github.com/iamwithnail/miniature-barnacle.git weather
    cd weather
    pip install -r requirements.txt
    python manage.py collectstatic 
    python manage.py makemigrations 
    python manage.py migrate
    python manage.py test
    
```

**Locally** run with 
```
python manage.py runserver 
```

**In production** we recommend running Gunicorn behind an NGINX reverse proxy.   

Although the repo will run with defaults, these are publicly available and therefore not secure.  You should [set environment variables](https://www.digitalocean.com/community/tutorials/how-to-read-and-set-environmental-and-shell-variables-on-a-linux-vps) for DJANGO_DEBUG, DJANGO_SECRET_KEY and OPEN_WEATHER_APP_ID.
OpenWeatherMap.org has free keys available.   

```
  pip install gunicorn 
```
from main directory (containing manage.py)
```
../env/bin/gunicorn -b 127.0.0.1:8081 -w 2 weather.wsgi:application 
```

**Usage**

API uses the openweathermap.org API to return weather data for a city location.  This API returns the mean, median, minimum and maximums of both temperature and humidity.  

Requests are in the format: 
```
/{url%20encoded%20%20city%20name}/{number_of_days}/
```
number_of_days should be an integer between 1 and 16 (the maximum number of days available from OpenWeather).  Note the trailing slash.  URLs will result in a 404 response if the trailing slash is omitted. 
If number of days is not provided, it will default to three.  
The OpenWeatherAPI will match almost anything, including some Unicode characters.  Hashes `%23` are not allowed and will throw a 400 Bad Request from Browseable API, and a 404 from programmatic access (see below). 

#To do
- Lack of testing of graph validity is unsatisfactory - pyquery installed to allow some length checking for axes, etc, but not yet implemented.  
- Investigate divergence between Unit test on url encoded hashes and manually checked browsers.  Former truncates the URL and gives a 404, latter trips the validation and correctly returns 400 Bad Request with appropriate detail. Neither processes the hash (as desired).  
- Improve test coverage - currently 76%, largely driven by lack of graph testing. 
- Migrate to Py3 - the numpy (very heavyweight and large) dependency could be resolved using Python3. 
- Odd behaviour around leading slash for / root URL (being deprecated in 1.10) - unittests resolve this to / when no leading slash present in urls.py, but browser correctly resolves to 404 handler.  

