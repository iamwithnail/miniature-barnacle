# miniature-barnacle

**Installation** 
```
    Virtualenv env
    source env/bin/activate
    git clone https://github.com/iamwithnail/miniature-barnacle.git 
    cd weather
    pip install -r requirements.txt
    python manage.py collectstatic 
```

**Locally** run with ```python manage.py runserver 
    
In production run with Gunicorn 
```
  pip install gunicorn 
```
from main directory (containing manage.py)
```
../env/bin/gunicorn -b 127.0.0.1:8081 -w 3 core.wsgi:application 


