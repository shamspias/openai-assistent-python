import json
import os
import gpt3_tokenizer
from typing import Optional


class ThreadManager:
    def __init__(self, client):
        self.client = client

    async def list_messages(self, thread_id: str, limit: int = 20, order: str = 'desc', after: Optional[str] = None,
                            before: Optional[str] = None):
        try:
            return await self.client.beta.threads.messages.list(thread_id=thread_id,
                                                                limit=limit,
                                                                order=order,
                                                                after=after,
                                                                before=before
                                                                )
        except Exception as e:
            print(f"An error occurred while retrieving messages: {e}")
            return None

    async def retrieve_message(self, thread_id: str, message_id: str):
        return await self.client.beta.threads.messages.retrieve(thread_id=thread_id, message_id=message_id)

    async def create_thread(self, messages: Optional[list] = None, metadata: Optional[dict] = None):
        return await self.client.beta.threads.create(messages=messages, metadata=metadata)

    async def retrieve_thread(self, thread_id: str):
        return await self.client.beta.threads.retrieve(thread_id)

    async def modify_thread(self, thread_id: str, metadata: dict):
        return await self.client.beta.threads.modify(thread_id, metadata=metadata)

    async def delete_thread(self, thread_id: str):
        return await self.client.beta.threads.delete(thread_id)

    async def send_message(self, thread_id: str, content: str, role: str = "user"):
        # token_count = self.count_tokens(content)
        # print(f"Tokens used in message: {token_count}")
        return await self.client.beta.threads.messages.create(thread_id=thread_id, role=role, content=content)

    async def create_run(self, thread_id: str, assistant_id: str):
        return await self.client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id)

    async def list_runs(self, thread_id: str):
        return await self.client.beta.threads.runs.list(thread_id=thread_id)

    @staticmethod
    def count_tokens(text: str):
        # Placeholder for the actual token counting logic
        return gpt3_tokenizer.count_tokens(text)

    @staticmethod
    def read_thread_data(filename: str = 'data.json'):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                return json.load(file)
        return {}

    @staticmethod
    def save_thread_data(thread_id: str, filename: str = 'data.json'):
        data = {'thread_id': thread_id}
        with open(filename, 'w') as file:
            json.dump(data, file)
