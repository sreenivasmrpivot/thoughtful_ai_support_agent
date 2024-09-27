# # Step 1: Install PDM
# pip install pdm

# # Step 2: Initialize project
# pdm init

# # Step 3: Add project details
# pdm config project.name thoughtful_ai_support_agent
# pdm config project.version 0.1.0
# pdm config project.description "A customer support AI Agent for Thoughtful AI using Gradio and LangChain."
# pdm config project.authors '["Your Name <your.email@example.com>"]'
# pdm config project.license.text MIT
# pdm config project.urls.Homepage "https://github.com/yourusername/thoughtful_ai_support_agent"

# Step 4: Add dependencies
# pdm config project.requires-python ">=3.12"
pdm add python-dotenv gradio setuptools langchain langchain_community langchain_openai openai faiss-cpu numpy scikit-learn tiktoken

# Step 5: Add optional dependencies
pdm add -G test pytest pytest-cov requests selenium playwright pytest-asyncio
pdm add -G dev ruff pyright pdm-pep517 pre-commit 

# Step 6: Install playright dependencies
pdm run playwright install
