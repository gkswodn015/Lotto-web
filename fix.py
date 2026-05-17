content = "#!/bin/sh\nset -e\n\necho 'Waiting for DB...'\nsleep 5\n\necho 'Running migrate...'\npython manage.py migrate --noinput\n\necho 'Collecting static...'\npython manage.py collectstatic --noinput\n\necho 'Starting server...'\nexec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3\n"

with open('docker/entrypoint.sh', 'w', newline='\n') as f:
    f.write(content)
print('done')