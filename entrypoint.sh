#!/bin/bash
set -e

echo "Waiting for PostgreSQL to be ready..."
while ! nc -z postgres 5432; do
  sleep 1
done
echo "PostgreSQL is ready!"

echo "Running migrations..."
python manage.py migrate --noinput

echo "Creating superuser admin/admin..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@agrodoc.local', 'admin')
    print('Superuser admin created')
else:
    u = User.objects.get(username='admin')
    u.set_password('admin')
    u.save()
    print('Superuser admin password updated')
"

echo "Loading initial reference data..."
python manage.py init_data || true

echo "Setup complete! Starting server..."
exec "$@"
