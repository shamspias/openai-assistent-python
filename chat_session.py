import asyncio
from thread_manager import ThreadManager
from assistant_manager import AssistantManager


class ChatSession:
    def __init__(self, thread_manager: ThreadManager, assistant_manager: AssistantManager, assistant_name: str,
                 model_name: str, assistant_id: str = None, thread_id: str = None):
        self.thread_manager = thread_manager
        self.assistant_manager = assistant_manager
        self.assistant_name = assistant_name
        self.model_name = model_name
        self.assistant_id = assistant_id
        self.thread_id = thread_id

    async def start_session(self):
        if self.thread_id is None:
            # Get or create a thread
            self.thread_id = await self.get_or_create_thread()

        if self.assistant_id is None:
            # Find or create an assistant
            self.assistant_id = await self.find_or_create_assistant(
                name=self.assistant_name,
                model=self.model_name
            )

        # Display existing chat history
        await self.display_chat_history()

        prev_messages = await self.thread_manager.list_messages(self.thread_id)
        if prev_messages is None:
            print("An error occurred while retrieving messages.")
            return

        # Start the chat loop
        await self.chat_loop()

    async def chat_loop(self):
        try:
            while True:
                user_input = input("You: ")
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    break
                if user_input.lower() in ['/delete', '/clear']:
                    await self.thread_manager.delete_thread(self.thread_id)
                    self.thread_id = await self.get_or_create_thread()
                    continue

                response = await self.get_latest_response(user_input)

                if response:
                    print("Assistant:", response)

        finally:
            print(f"Session ended")

    async def get_or_create_thread(self):
        data = self.thread_manager.read_thread_data()
        thread_id = data.get('thread_id')
        if not thread_id:
            thread = await self.thread_manager.create_thread(messages=[])
            thread_id = thread.id
            self.thread_manager.save_thread_data(thread_id)
        return thread_id

    async def find_or_create_assistant(self, name: str, model: str):
        """
        Finds an existing assistant by name or creates a new one.

        Args:
            name (str): The name of the assistant.
            model (str): The model ID for the assistant.

        Returns:
            str: The ID of the found or created assistant.
        """
        assistant_id = await self.assistant_manager.get_assistant_id_by_name(name)
        if not assistant_id:
            assistant = await self.assistant_manager.create_assistant(name=name,
                                                                      model=model,
                                                                      instructions="",
                                                                      tools=[{"type": "retrieval"}]
                                                                      )
            assistant_id = assistant.id
        return assistant_id

    async def send_message(self, content):
        return await self.thread_manager.send_message(self.thread_id, content)

    async def display_chat_history(self):
        messages = await self.thread_manager.list_messages(self.thread_id)
        if messages is None:
            return
        print(messages)
        for message in reversed(messages.data):
            role = message.role
            content = message.content[0].text.value  # Assuming message content is structured this way
            print(f"{role.title()}: {content}")

    async def get_latest_response(self, user_input):
        # Send the user message
        await self.send_message(user_input)

        # Create a new run for the assistant to respond
        await self.create_run()

        # Wait for the assistant's response
        await self.wait_for_assistant()

        # Retrieve the latest response
        return await self.retrieve_latest_response()

    async def create_run(self):
        return await self.thread_manager.create_run(self.thread_id, self.assistant_id)

    async def wait_for_assistant(self):
        while True:
            runs = await self.thread_manager.list_runs(self.thread_id)
            latest_run = runs.data[0]
            if latest_run.status in ["completed", "failed"]:
                break
            await asyncio.sleep(2)  # Wait for 2 seconds before checking again

    async def retrieve_latest_response(self):
        response = await self.thread_manager.list_messages(self.thread_id)
        for message in response.data:
            if message.role == "assistant":
                return message.content[0].text.value
        return None
