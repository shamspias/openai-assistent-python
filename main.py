import asyncio
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from thread_manager import ThreadManager
from assistant_manager import AssistantManager
from chat_session import ChatSession

# Load environment variables from .env file
load_dotenv()

# Use the environment variables
API_KEY = os.getenv('API_KEY')
ASSISTANT_NAME = os.getenv('ASSISTANT_NAME')
ASSISTANT_ID = os.getenv('ASSISTANT_ID')
MODEL_NAME = os.getenv('MODEL_NAME')


# ASSISTANT_ID will be fetched dynamically after creation or during the session

# Entry point
async def main():
    # Initialize the OpenAI async client
    openai_async_client = AsyncOpenAI(api_key=API_KEY)

    # Create instances of manager classes with the OpenAI client
    thread_manager = ThreadManager(openai_async_client)
    assistant_manager = AssistantManager(openai_async_client)

    # Start a chat session with the assistant name and model name
    chat_session = ChatSession(thread_manager, assistant_manager, ASSISTANT_NAME, MODEL_NAME, ASSISTANT_ID)
    await chat_session.start_session()


if __name__ == "__main__":
    asyncio.run(main())
