#!/usr/bin/env bash
set -euo pipefail

# Wait for Postgres
python - <<'PY'
import os, time, re
import psycopg2
url = os.environ.get('DATABASE_URL', '')
if not url:
    raise SystemExit('DATABASE_URL not set')
m = re.match(r"postgresql\+psycopg2://([^:]+):([^@]+)@([^:]+):(\d+)/(\S+)", url)
if not m:
    raise SystemExit(f'Bad DATABASE_URL: {url}')
user, pwd, host, port, db = m.groups()
for _ in range(60):
    try:
        psycopg2.connect(dbname=db, user=user, password=pwd, host=host, port=port).close()
        break
    except Exception:
        time.sleep(1)
else:
    raise SystemExit('Postgres not ready')
PY

# Run migrations
flask db upgrade

# Start server
exec flask run --host=0.0.0.0 --port=5000
