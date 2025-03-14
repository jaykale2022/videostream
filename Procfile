web: gunicorn project1.wsgi --log-file - 
#or works good with external database
web: python manage.py migrate && gunicorn project1.wsgi