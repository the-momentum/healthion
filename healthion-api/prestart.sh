#!/bin/bash
set -e -x

until uv run python -u scripts/healthchecks/db_up_check.py
do
  echo 'Waiting for db services to become available...'
  sleep 1
done
echo 'DB containers UP, proceeding...'

exec "$@"
