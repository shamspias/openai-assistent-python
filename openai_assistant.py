import openai


class OpenAIAssistantError(Exception):
    """Custom exception class for OpenAIAssistant errors."""
    pass


class OpenAIAssistant:
    def __init__(self, client):
        self.client = client

    def get_assistant_by_name(self, name):
        try:
            assistants = self.client.beta.assistants.list().data
            return next((assistant for assistant in assistants if assistant['name'] == name), None)
        except Exception as e:
            raise OpenAIAssistantError(f"An error occurred while retrieving assistants: {e}")

    def create_assistant(self, name, model, description=None, tools=None, file_ids=None):
        try:
            return self.client.beta.assistants.create(
                name=name,
                model=model,
                description=description,
                tools=tools,
                file_ids=file_ids
            )
        except Exception as e:
            raise OpenAIAssistantError(f"An error occurred while creating an assistant: {e}")

    def create_or_get_assistant(self, name, model, description=None, tools=None, file_ids=None):
        assistant = self.get_assistant_by_name(name)
        if assistant:
            return assistant
        return self.create_assistant(name, model, description, tools, file_ids)

    def delete_assistant(self, assistant_id):
        try:
            self.client.beta.assistants.delete(assistant_id)
        except Exception as e:
            raise OpenAIAssistantError(f"An error occurred while deleting an assistant: {e}")

    def list_assistants(self):
        try:
            return self.client.beta.assistants.list().data
        except Exception as e:
            raise OpenAIAssistantError(f"An error occurred while listing assistants: {e}")

    def create_thread(self, assistant_id, initial_message, file_ids=None):
        try:
            return self.client.beta.threads.create(
                assistant_id=assistant_id,
                messages=[
                    {
                        "role": "user",
                        "content": initial_message,
                        "file_ids": file_ids or []
                    }
                ]
            )
        except Exception as e:
            raise OpenAIAssistantError(f"An error occurred while creating a thread: {e}")

    def delete_thread(self, thread_id):
        try:
            self.client.beta.threads.delete(thread_id)
        except Exception as e:
            raise OpenAIAssistantError(f"An error occurred while deleting a thread: {e}")

    def list_threads(self, assistant_id):
        try:
            return self.client.beta.threads.list(assistant_id=assistant_id).data
        except Exception as e:
            raise OpenAIAssistantError(f"An error occurred while listing threads: {e}")

    def chat_with_assistant(self, thread_id, message, file_ids=None):
        try:
            return self.client.beta.threads.messages.create(
                thread_id=thread_id,
                messages=[
                    {
                        "role": "user",
                        "content": message,
                        "file_ids": file_ids or []
                    }
                ]
            )
        except Exception as e:
            raise OpenAIAssistantError(f"An error occurred while chatting with the assistant: {e}")

    def handle_command(self, command, thread_id=None, assistant_id=None):
        try:
            if command == "/clear" and thread_id:
                self.delete_thread(thread_id)
                return "Thread deleted."
            elif command == "/delete" and assistant_id:
                self.delete_assistant(assistant_id)
                return "Assistant deleted."
            else:
                return "Invalid command."
        except OpenAIAssistantError as e:
            return str(e)

# Example usage to test:
# client = openai.Client(api_key='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')
# assistant = OpenAIAssistant(client)
# assistant.create_or_get_assistant('MyAssistant', 'gpt-4-1106-preview')
