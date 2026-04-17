@echo off
chcp 65001 >nul
title AgroDoc — Deploy

cd /d c:\IT\AgroDoc-System

echo.
echo ==========================================
echo   AgroDoc — сборка и перезапуск Docker
echo ==========================================
echo.

REM --- опциональный git pull ---
set /p PULL="Git pull перед сборкой? [y/N]: "
if /i "%PULL%"=="y" (
    echo.
    echo [git] Получаю изменения...
    git pull
    if %errorlevel% neq 0 (
        echo ОШИБКА: git pull не удался
        pause
        exit /b 1
    )
    echo.
)

REM --- сборка только тех сервисов, которые меняются ---
echo [1/3] Сборка backend и frontend...
docker compose build agrodb_web agrodb_frontend
if %errorlevel% neq 0 (
    echo.
    echo ОШИБКА: сборка завершилась с ошибкой. Смотри лог выше.
    pause
    exit /b 1
)

echo.
echo [2/3] Перезапуск сервисов...
docker compose up -d agrodb_web agrodb_frontend agrodb_nginx
if %errorlevel% neq 0 (
    echo.
    echo ОШИБКА: запуск не удался
    pause
    exit /b 1
)

echo.
echo [3/3] Жду старта (5 сек.)...
timeout /t 5 /nobreak >nul

echo.
echo ==========================================
echo   Готово! http://192.168.1.155
echo ==========================================
echo.

start https://192.168.1.71/

echo.
echo Логи backend (Ctrl+C — выход из логов, контейнер продолжит работу):
echo.
docker compose logs -f agrodb_web
