#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput

if [ "${RUN_SUPERUSER}" = "1" ]; then
    python manage.py create_default_superuser || true
fi
