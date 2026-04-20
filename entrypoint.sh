#!/bin/bash
set -e

echo "Waiting for PostgreSQL to be ready..."
while ! nc -z postgres 5432; do
  sleep 1
done
echo "PostgreSQL is ready!"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Creating Django superuser for admin panel..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@agrodoc.local', 'admin123')
    print('Django superuser created')
else:
    print('Django superuser already exists')
"

echo "Initialising accounts..."
python manage.py init_data || true

echo "Setup complete! Starting server..."
exec "$@"
