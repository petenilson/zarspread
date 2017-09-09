web: gunicorn zarspread.wsgi
main_worker: celery --app=zarspread worker --beat --loglevel=INFO
