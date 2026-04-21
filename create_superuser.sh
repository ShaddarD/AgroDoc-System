#!/bin/bash

echo "=== Создание суперпользователя ==="
echo

# Получаем данные от пользователя
read -p "Введите имя пользователя (default: admin): " username
username=${username:-admin}

read -p "Введите email: " email
email=${email:-admin@agrodoc.local}

read -s -p "Введите пароль: " password
echo
read -s -p "Подтвердите пароль: " password_confirm
echo

if [ "$password" != "$password_confirm" ]; then
    echo "Пароли не совпадают!"
    exit 1
fi

# Создаем суперпользователя через Django shell
docker compose exec agrodb_web python manage.py shell << EOF
from django.contrib.auth.models import User

if User.objects.filter(username='$username').exists():
    print(f"Пользователь '{$username}' уже существует!")
else:
    User.objects.create_superuser('$username', '$email', '$password')
    print(f"✅ Суперпользователь '{$username}' создан успешно!")
EOF

echo
echo "=== Готово ==="
echo "Логин: $username"
echo "Email: $email"
echo
echo "Доступ к админ-панели: http://localhost/admin"
