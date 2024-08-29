class ChatHistory:
    def __init__(self):
        self.messages = []

    def __str__(self):
        return "\n".join(["{}: {}".format(msg['role'], msg['content']) for msg in self.messages])  

    def __iter__(self):
        return iter(self.messages)

    def add_user_message(self, content):
        self.messages.append({
            "role": "user",
            "content": content
        })

    def add_assistant_message(self, content):
        self.messages.append({
            "role": "assistant",
            "content": content
        })
