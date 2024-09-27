# scripts/run_all.zsh

#!/bin/zsh

# Exit immediately if a command exits with a non-zero status
set -e

echo "=== Running Pre-commit Hooks Locally ==="
# pdm run pre-commit run --all-files

echo "\n=== Running Tests Locally ==="
pdm run test

echo "\n=== Running Linting ==="
pdm run lint

echo "\n=== Running Type Checking ==="
pdm run type-check

echo "\n=== Generating Coverage Report ==="
pdm run coverage

echo "\n=== Running Tests in Docker Compose ==="
docker-compose up --build --abort-on-container-exit
