@echo off
chcp 65001 >nul
title AgroDoc — Deploy

cd /d c:\IT\AgroDoc-System

echo.
echo ==========================================
echo   AgroDoc — деплой на локальный Docker
echo ==========================================
echo.

REM --- git pull ---
echo [1/4] Получаю последние изменения из Git...
git pull
if %errorlevel% neq 0 (
    echo.
    echo ОШИБКА: git pull не удался.
    echo Проверь конфликты или подключение к сети.
    pause
    exit /b 1
)
echo.

REM --- сборка backend и frontend ---
echo [2/4] Сборка контейнеров (backend + frontend)...
docker compose build agrodb_web agrodb_frontend
if %errorlevel% neq 0 (
    echo.
    echo ОШИБКА: сборка завершилась с ошибкой. Смотри лог выше.
    pause
    exit /b 1
)
echo.

REM --- перезапуск ---
echo [3/4] Перезапуск сервисов...
docker compose up -d agrodb_web agrodb_frontend agrodb_nginx
if %errorlevel% neq 0 (
    echo.
    echo ОШИБКА: запуск контейнеров не удался.
    pause
    exit /b 1
)
echo.

REM --- ждём старта и показываем статус ---
echo [4/4] Жду старта (6 сек.)...
timeout /t 6 /nobreak >nul

echo.
echo ==========================================
echo   Статус контейнеров:
echo ==========================================
docker compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"

echo.
echo ==========================================
echo   Готово!  https://192.168.1.71/
echo ==========================================
echo.

start https://192.168.1.71/

echo Логи backend — Ctrl+C для выхода (контейнер продолжит работать):
echo.
docker compose logs -f agrodb_web
