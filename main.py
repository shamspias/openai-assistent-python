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
    assistant_id = os.getenv('ASSISTANT_ID')
    assistant_name = os.getenv('ASSISTANT_NAME')
    file_ids = os.getenv('FILE_IDS', '').split(',') if os.getenv('FILE_IDS') else []

    openai_client = openai.Client(api_key=api_key)
    assistant_manager = OpenAIAssistant(openai_client)
    chat_interface = TerminalChatInterface(
        assistant_manager,
        assistant_id=assistant_id,
        assistant_name=assistant_name,
        file_ids=file_ids
    )
    chat_interface.start_chat()


if __name__ == "__main__":
    main()
