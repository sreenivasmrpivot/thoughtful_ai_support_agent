# Thoughtful AI Support Agent

A comprehensive customer support AI Agent for Thoughtful AI that assists users with basic questions using predefined responses and falls back to a language model for other queries. The application leverages asynchronous programming with `asyncio` to enhance performance and responsiveness.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Setup](#setup)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Install PDM](#2-install-pdm)
  - [3. Install Dependencies](#3-install-dependencies)
  - [4. Set Environment Variables](#4-set-environment-variables)
  - [5. Initialize Pre-commit Hooks](#5-initialize-pre-commit-hooks)
- [Running the Application](#running-the-application)
  - [1. Locally](#1-locally)
  - [2. Using Docker](#2-using-docker)
- [Testing](#testing)
  - [1. Running Tests Locally](#1-running-tests-locally)
  - [2. Running Tests in Docker](#2-running-tests-in-docker)
- [Deployment](#deployment)
  - [1. Deploy to Repl.it](#1-deploy-to-replit)
  - [2. Deploy to Kubernetes](#2-deploy-to-kubernetes)
- [Git Commands](#git-commands)
- [Code Quality Tools](#code-quality-tools)
- [Additional Notes](#additional-notes)

## Features

- **Predefined Responses**: Responds to common questions using a predefined dataset.
- **Fallback Mechanism**: Uses OpenAI's GPT-4 to handle unknown queries.
- **Web-Based Chat Interface**: Interactive UI built with Gradio.
- **Asynchronous Programming**: Enhanced performance with `asyncio`.
- **Modular Design**: Organized using object-oriented principles.
- **Comprehensive Testing**: Includes unit, integration, and end-to-end tests.
- **Pre-commit Hooks**: Ensures code quality through linting, formatting, type checking, and testing.
- **Containerization**: Docker support for consistent deployments.
- **Kubernetes Ready**: Deployment artifacts for Kubernetes orchestration.
- **Deployment to Repl.it**: Easy deployment on Repl.it platform.
- **Code Quality Tools**: Ruff for linting and formatting, Pyright for type checking.
- **Code Coverage**: Ensures robust testing coverage.

## Project Structure





---

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/thoughtful_ai_support_agent.git
cd thoughtful_ai_support_agent
```

### 2. Install PDM
`PDM` is a modern Python package manager. Install it using `pip`:

```bash
pip install pdm
```

### 3. Install Dependencies
Initialize the project and install dependencies:

```bash
pdm install
pdm install -G test
pdm install -G dev
```

### 4. Set Environment Variables
Ensure you have an OpenAI API key. Set it as an environment variable:

```bash
export OPENAI_API_KEY='your-openai-api-key'
```

On Windows:

```cmd
set OPENAI_API_KEY=your-openai-api-key
```

Note for Repl.it Deployment: Repl.it forwards port `8080` by default. Therefore, set the `PORT` environment variable accordingly when deploying to Repl.it.

### 5. Initialize Pre-commit Hooks
Pre-commit hooks ensure code quality by running specified checks before code is committed.

```bash
pdm run pre-commit install
```

This command sets up the Git hooks defined in `.pre-commit-config.yaml`.

## Running the Application

### 1. Locally
Run the application using the provided Zsh script:

```bash
./scripts/run_all.zsh
```

Alternatively, you can run it directly:

```bash
pdm run start
```

Access the chat interface via http://localhost:7860.

### 2. Using Docker
#### Build the Docker Image:

```bash
docker build -t thoughtful-ai-support-agent .
```

#### Run the Docker Container:

```bash
docker run -d -p 7860:7860 -e OPENAI_API_KEY='your-openai-api-key' --name ai_support_agent thoughtful-ai-support-agent
```

Access the application via http://localhost:7860.

#### Using Docker Compose:

Run all services defined in docker-compose.yml:

```bash
docker-compose up --build
```

Note: Ensure that the `.env file` contains the `OPENAI_API_KEY` if you choose to use environment variable files with Docker Compose.

## Testing

### 1. Running Tests Locally
Use the provided Zsh script to run all tests, linting, type checking, and coverage:

```bash
./scripts/run_all.zsh
```

Alternatively, run tests manually:

```bash
pdm run test
```

### 2. Running Tests in Docker
The run_all.zsh script also runs tests within Docker Compose. Ensure Docker is running and execute:

```bash
./scripts/run_all.zsh
```

## Deployment

### 1. Deploy to Repl.it
Repl.it allows you to run your application in the cloud effortlessly.

#### Steps:
1. Create a New Repl:

    Go to Repl.it and create a new Python Repl.

2. Upload Project Files:

    Upload all necessary files as per the project structure.

3. Configure Environment Variables:

    Set `OPENAI_API_KEY` and `PORT=8080` in the Secrets tab.

4. Install PDM and Dependencies:

    * In the Repl shell, run:

        ```bash
        pip install pdm
        pdm config python.use_pyenv false
        pdm install
        ```

5. Adjust Port Configuration:

    * Repl.it forwards port 8080. Ensure your application reads the PORT environment variable.

6. Set Run Command:

    * Create a .replit file with the following content:

    ```ini
    run = "pdm run start"
    ```

7. Run the Repl:

    * Click "Run" and access the application via the provided URL.

#### Updated deploy_repl.zsh Script:

Ensure that the deploy_repl.zsh script sets the PORT environment variable to 8080 when deploying to Repl.it.

```zsh
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

# Set PORT to 8080 for Repl.it
export PORT=8080

# Run the application
echo "Starting the application..."
pdm run start
```

#### Make the script executable:

```bash
chmod +x scripts/deploy_repl.zsh
```

### 2. Deploy to Kubernetes
Deploy the application to a Kubernetes cluster using provided manifests.

#### Steps:
1. Apply Namespace:

```bash
kubectl apply -f kubernetes/namespace.yaml
```

2. Apply Secret:

Encode your OpenAI API key in base64:

```bash
echo -n 'your-openai-api-key' | base64
```

3. Replace <base64-encoded-key> in kubernetes/secret.yaml with the encoded key and apply:

```bash
kubectl apply -f kubernetes/secret.yaml
```

4. Apply Deployment and Service:

```bash
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
```

5. Apply Ingress (Optional):

If you have an Ingress controller set up, apply the ingress manifest:

```bash
kubectl apply -f kubernetes/ingress.yaml
```

6. Verify Deployment:

```bash
kubectl get all -n thoughtful-ai
```

7. Use the provided deployment script:

Run the deploy_k8s.zsh script to automate the deployment process.

```bash
./scripts/deploy_k8s.zsh
```

8. Make the script executable:

```bash
chmod +x scripts/deploy_k8s.zsh
```

## Git Commands

1. Initialize Git Repository

```bash
git init
```

2. Add Remote Repository
Replace yourusername and yourrepository with your GitHub username and repository name.

```bash
git remote add origin https://github.com/yourusername/thoughtful_ai_support_agent.git
```

3. Add All Files to Git

```bash
git add .
```

4. Commit the Changes

```bash
git commit -m "Initial commit: Set up Thoughtful AI Support Agent with asyncio"
```

5. Push to GitHub

```bash
git branch -M main
git push -u origin main
```

Note: Ensure that the repository thoughtful_ai_support_agent exists on GitHub. You can create it via GitHub's web interface before pushing.

## Code Quality Tools

1. Linting with Ruff

    Run Ruff to lint the code:

    ```bash
    pdm run lint
    ```

2. Type Checking with Pyright

    Run Pyright to perform type checking:

    ```bash
    pdm run type-check
    ```

3. Code Coverage

    Generate and view the coverage report:

    ```bash
    pdm run coverage
    ```

    Open `htmlcov/index.html` in your browser to see detailed coverage.

4. Pre-commit Hooks

    Ensure all code adheres to quality standards before committing.

    Run Pre-commit Hooks Manually:

    ```bash
    pdm run pre-commit run --all-files
    ```
## Optional Instructions

1. Remove the current lock file:

    ```bash
    rm pdm.lock
    ```

2. Clear PDM cache:

    ```bash
    pdm cache clear
    ```
