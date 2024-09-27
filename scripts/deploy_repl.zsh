# scripts/deploy_repl.zsh

#!/bin/zsh

# Exit immediately if a command exits with a non-zero status
set -e

echo "=== Deploying to Repl.it ==="

# Ensure PDM is installed
if ! command -v pdm &> /dev/null
then
    echo "PDM could not be found. Installing PDM..."
    pip install pdm
fi

# Install dependencies
echo "Installing dependencies..."
pdm install
pdm install -G test
pdm install -G dev

# Run the application
echo "Starting the application..."
pdm run start
