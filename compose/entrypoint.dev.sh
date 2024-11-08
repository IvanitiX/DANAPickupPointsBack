#!/bin/bash
set -e

echo "Test"

host="$DB_HOST"

echo "Connecting to $host ..."

until nc -z "$host" 5432; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"

python src/manage.py migrate
python src/manage.py collectstatic --noinput
python src/manage.py runserver 0.0.0.0:8000