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
echo [1/4] git pull...
git pull
if %errorlevel% neq 0 (
    echo.
    echo ОШИБКА на шаге 1: git pull не удался
    pause
    exit /b 1
)
echo OK
echo.

REM --- сборка ---
echo [2/4] Сборка контейнеров (может занять 1-3 мин.)...
docker compose build agrodb_web agrodb_frontend
if %errorlevel% neq 0 (
    echo.
    echo ОШИБКА на шаге 2: сборка не удалась — смотри лог выше
    pause
    exit /b 1
)
echo OK
echo.

REM --- перезапуск ---
echo [3/4] Перезапуск сервисов...
docker compose up -d agrodb_web agrodb_frontend agrodb_nginx
if %errorlevel% neq 0 (
    echo.
    echo ОШИБКА на шаге 3: запуск не удался
    pause
    exit /b 1
)
echo OK
echo.

REM --- статус ---
echo [4/4] Жду старта (6 сек.)...
timeout /t 6 /nobreak >nul

echo.
docker compose ps --format "table {{.Name}}\t{{.Status}}\t{{.Ports}}"

echo.
echo ==========================================
echo   Готово!  http://192.168.1.71/
echo ==========================================
echo.

start http://192.168.1.71/

echo Логи backend (Ctrl+C — выход, контейнер продолжит работать):
echo.
docker compose logs -f agrodb_web
