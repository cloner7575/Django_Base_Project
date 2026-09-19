#!/bin/sh
set -e

echo "Waiting for database..."
python - <<'PY'
import os, time
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.environ.get("DJANGO_SETTINGS_MODULE", "core.settings.production"))
django.setup()
from django.db import connection
from django.db.utils import OperationalError
for i in range(30):
    try:
        connection.ensure_connection()
        break
    except OperationalError:
        time.sleep(1)
else:
    raise SystemExit("Database unavailable")
PY

python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec "$@"
