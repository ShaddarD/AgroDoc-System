Write-Host "Stopping old containers..."
docker compose down

Write-Host "Rebuilding images..."
docker compose build --no-cache

Write-Host "Starting containers..."
docker compose up -d

Write-Host "Current status:"
docker compose ps