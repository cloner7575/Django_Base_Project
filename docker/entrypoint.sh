#!/bin/sh
set -eu

echo "Waiting for database..."
python - <<'PY'
import os
import time
from urllib.parse import urlparse

import psycopg

url = os.environ.get("DATABASE_URL", "")
parsed = urlparse(url)
if parsed.scheme.startswith("postgres"):
    for attempt in range(30):
        try:
            with psycopg.connect(
                dbname=parsed.path.lstrip("/"),
                user=parsed.username,
                password=parsed.password,
                host=parsed.hostname,
                port=parsed.port or 5432,
                connect_timeout=3,
            ):
                break
        except Exception:
            time.sleep(1)
    else:
        raise SystemExit("Database not ready")
PY

python manage.py migrate --noinput
python manage.py collectstatic --noinput
exec "$@"
