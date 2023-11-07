# main.py
import os
from dotenv import load_dotenv
import openai
from openai_assistant import OpenAIAssistant
from chat_interface import TerminalChatInterface

# Load environment variables from .env file
load_dotenv()


def main():
    api_key = os.getenv('OPENAI_API_KEY')
    assistant_id = os.getenv('ASSISTANT_ID')  # Assuming you have an ASSISTANT_ID in your .env
    assistant_name = os.getenv('ASSISTANT_NAME')  # Assuming you also have an ASSISTANT_NAME in your .env
    # If you don't have an ASSISTANT_ID or ASSISTANT_NAME, you can create a new assistant with:
    # assistant_manager.create_assistant() and just use ASSISTANT_NAME for it

    openai_client = openai.Client(api_key=api_key)
    assistant_manager = OpenAIAssistant(openai_client)
    chat_interface = TerminalChatInterface(assistant_manager, assistant_id=assistant_id, assistant_name=assistant_name)
    chat_interface.start_chat()


if __name__ == "__main__":
    main()
