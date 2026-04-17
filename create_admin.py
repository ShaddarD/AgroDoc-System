from django.contrib.auth.models import User

# Проверяем существующих суперпользователей
admins = User.objects.filter(is_superuser=True)
if admins.exists():
    print("✅ Существующие суперпользователи:")
    for admin in admins:
        print(f"   - {admin.username} ({admin.email})")
else:
    print("❌ Суперпользователей не найдено")
    
# Создаем нового суперпользователя
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@agrodoc.local', 'admin')
    print("✅ Суперпользователь 'admin' создан с паролем 'admin'")
else:
    print("⚠️  Пользователь 'admin' уже существует")
    # Обновляем пароль
    user = User.objects.get(username='admin')
    user.set_password('admin')
    user.save()
    print("✅ Пароль обновлен на 'admin'")
