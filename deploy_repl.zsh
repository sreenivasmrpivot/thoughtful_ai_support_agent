#!/bin/zsh

# Exit immediately if a command exits with a non-zero status
set -e

# Function to print informational messages
function echo_info() {
    echo "\033[1;34m[INFO]\033[0m $1"
}

# Function to print error messages
function echo_error() {
    echo "\033[1;31m[ERROR]\033[0m $1"
}

# 1. Check if PDM is installed; install if not
if ! command -v pdm &> /dev/null
then
    echo_info "PDM not found. Installing PDM..."
    curl -sSL https://install.pdm.fming.dev | python3 -
    # Add PDM to PATH for the current session
    export PATH="$HOME/.local/bin:$PATH"
    echo_info "PDM installed successfully."
else
    echo_info "PDM is already installed."
fi

# 2. Install project dependencies using PDM
echo_info "Installing project dependencies with PDM..."
pdm install

# 3. Export dependencies to requirements.txt for Repl.it compatibility
echo_info "Exporting dependencies to requirements.txt..."
pdm export -f requirements > requirements.txt
echo_info "requirements.txt generated successfully."

# 4. Create start.sh script to launch the Gradio app on Repl.it
echo_info "Creating start.sh script..."
cat <<EOL > start.sh
#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Install PDM if not already installed
if ! command -v pdm &> /dev/null
then
    echo "[INFO] PDM not found. Installing PDM..."
    curl -sSL https://install.pdm.fming.dev | python3 -
    export PATH="\$HOME/.local/bin:\$PATH"
    echo "[INFO] PDM installed."
fi

# Install dependencies using PDM
echo "[INFO] Installing dependencies with PDM..."
pdm install

# Launch the Gradio app
echo "[INFO] Starting the Gradio app..."
pdm run python src/ui.py
EOL

# Make start.sh executable
chmod +x start.sh
echo_info "start.sh created and made executable."

# 5. Create .replit file to configure Repl.it run settings
echo_info "Creating .replit configuration file..."
cat <<EOL > .replit
language = "python3"

run = "bash start.sh"
EOL
echo_info ".replit file created successfully."

# 6. Create .env file with placeholders for environment variables
echo_info "Creating .env file with placeholders for environment variables..."
cat <<EOL > .env
# Replace the placeholder with your actual OpenAI API key
OPENAI_API_KEY=your_openai_api_key_here

# These are default values; Repl.it provides the PORT environment variable automatically
PORT=7860
HOST=0.0.0.0
EOL
echo_info ".env file created. Please update the OpenAI API key in Repl.it's Secrets settings."

# 7. Create .gitignore to exclude .env and other unnecessary files
echo_info "Creating .gitignore file..."
cat <<EOL > .gitignore
# Ignore Python cache
__pycache__/
*.py[cod]

# Ignore environment files
.env

# Ignore PDM-related files
__pypackages__/
pdm.lock
EOL
echo_info ".gitignore file created successfully."

# 8. Provide final instructions to the user
echo_info "Deployment setup is complete."
echo_info "Follow these steps to deploy your app to Repl.it:"
echo_info "1. Initialize a git repository (if not already initialized):"
echo_info "   git init"
echo_info "2. Add all files to git and commit:"
echo_info "   git add ."
echo_info "   git commit -m 'Deploy Gradio app to Repl.it'"
echo_info "3. Push your repository to GitHub (if you haven't already):"
echo_info "   git remote add origin https://github.com/yourusername/your-repo.git"
echo_info "   git push -u origin master"
echo_info "4. Go to Repl.it and create a new Repl by importing your GitHub repository."
echo_info "5. In your Repl.it project, navigate to the 'Secrets' (Environment Variables) section and set the following variables:"
echo_info "   - OPENAI_API_KEY: your actual OpenAI API key"
echo_info "6. Click the 'Run' button in Repl.it to start your Gradio app."

echo_info "Your Gradio app should now be running on Repl.it!"
