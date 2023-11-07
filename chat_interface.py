class TerminalChatInterface:
    """A simple terminal interface to interact with an OpenAI Assistant."""

    def __init__(self, assistant_manager, assistant_id=None, assistant_name=None, file_ids=None):
        """
        Initialize the interface with an instance of OpenAIAssistant.
        If both assistant ID and name are provided, verify they match.
        """
        self.assistant_manager = assistant_manager
        self.assistant_id = assistant_id
        self.assistant_name = assistant_name
        self.file_ids = file_ids
        self.thread_id = None

        if assistant_id and assistant_name:
            self.verify_assistant_id_and_name_match()

    def verify_assistant_id_and_name_match(self):
        """Verify that the provided assistant ID and name correspond to the same assistant."""
        try:
            assistant = self.assistant_manager.get_assistant(self.assistant_id)
            if assistant['name'] != self.assistant_name:
                raise ValueError("The provided assistant ID and name do not correspond to the same assistant.")
        except Exception as e:
            print(f"An error occurred while verifying the assistant: {e}")
            exit()

    def start_chat(self):
        """Start the chatbot interface in the terminal."""
        if not self.assistant_id:
            print("No assistant ID could be found or provided. Exiting.")
            return

        print(f"Welcome to the OpenAI Chatbot Interface.")
        print(f"You are now chatting with assistant ID '{self.assistant_id}'.")
        self.start_thread()

    def start_thread(self):
        """Start a new thread for conversation with the assistant."""
        try:
            initial_message = "Hello, how can I assist you today?"
            thread = self.assistant_manager.create_thread(self.assistant_id, initial_message,
                                                          file_ids=self.file_ids)  # Updated
            self.thread_id = thread.get('id')
            print(f"Bot: {initial_message}")

            # Chat loop
            self.chat_loop()
        except Exception as e:
            print(f"An error occurred: {e}")
            exit()

    def chat_loop(self):
        """Loop to handle chat messages."""
        while True:
            user_message = input("You: ")
            if user_message == '/exit':
                print("Exiting the chat.")
                break
            elif user_message.startswith('/'):
                self.handle_command(user_message)
            else:
                try:
                    response = self.assistant_manager.chat_with_assistant(self.thread_id, user_message)
                    print(f"Bot: {response['choices'][0]['message']['content']}")
                except Exception as e:
                    print(f"An error occurred while sending the message: {e}")

    def handle_command(self, command):
        """Handle special commands in the chat interface."""
        parts = command.split()
        cmd = parts[0]
        data = parts[1] if len(parts) > 1 else None

        try:
            response = self.assistant_manager.handle_command(cmd, thread_id=self.thread_id,
                                                             assistant_id=self.assistant_id)
            print(response)
        except Exception as e:
            print(f"An error occurred while handling the command: {e}")
