Start it up::

    virtualenv ve -p /usr/bin/python3.6
    ./ve/bin/pip install -r requirements.txt
    ./ve/bin/python learning/manage.py migrate
    ./ve/bin/python learning/manage.py runserver
