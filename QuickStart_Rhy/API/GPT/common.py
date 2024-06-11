class GPTBotBase:
    def __init__(self, system_prompt, record_history=True):
        self.messages = [
            {
                "role": "system",
                "content": system_prompt,
            }
        ]
        self.record_history = record_history
    
    def save_conversation(self, file_path: str):
        with open(file_path, "w", encoding="utf-8") as f:
            for message in self.messages:
                f.write(f"{message['role']}\n\n{message['content']}\n---\n")
