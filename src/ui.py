# src/ui.py

import gradio as gr
import logging
from .data_loader import DataLoader
from .response_handler import ResponseHandler
from .chatbot import Chatbot
from .config import Config
import asyncio

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# The main Gradio app function
async def main():
    # Initialize configuration
    config = Config()

    # Initialize data loader
    data_loader = DataLoader(filepath='predefined_data.json')

    # Initialize response handler
    response_handler = ResponseHandler(
        questions=data_loader.get_questions(),
        answers=data_loader.get_answers(),
        config=config
    )

    # Initialize chatbot
    chatbot = Chatbot(response_handler=response_handler)

    # The respond function that processes user input and returns chatbot response
    async def respond(user_message: str, history) -> tuple:
        response = await chatbot.get_response(user_message)
        history = history or []  # If no history is provided, start with an empty list
        history.append((user_message, response))  # Append the user input and bot response
        return history, history  # Return two outputs as expected by Gradio

    # Gradio UI definition
    with gr.Blocks() as demo:
        gr.Markdown("## 🧠 Thoughtful AI Support Agent")

        # Define Gradio components
        chatbot_interface = gr.Chatbot()
        state = gr.State([])  # History of the conversation will be stored here

        with gr.Row():
            txt = gr.Textbox(
                show_label=False,
                placeholder="Type your message here and press Enter...",
            )

        # When the user submits the message, respond function will be triggered
        txt.submit(fn=respond, inputs=[txt, state], outputs=[chatbot_interface, state])

        # Clear the textbox after submission
        txt.submit(lambda: "", None, txt)

    # Launch the Gradio interface
    demo.launch(server_name=config.HOST, server_port=config.PORT, show_error=True)

# If the script is run directly, run the Gradio app with asyncio
if __name__ == "__main__":
    asyncio.run(main())
