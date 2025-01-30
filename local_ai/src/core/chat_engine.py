from pathlib import Path
from typing import Generator
import ollama
from ..utils.data_privacy import DataEncryptor
from ..models.multimodal import MultiModalProcessor
from ..utils.config_loader import load_config
import json
import time

class ChatEngine:
    def __init__(self):
        self.config = load_config()
        self.model_name = self.config['model']['default']
        self.temperature = self.config['model']['temperature']
        self.gpu_layers = self.config['model']['gpu_layers']
        self.max_history = self.config['model']['max_history']

        self.history = []
        self.attachments = []
        self.encryptor = DataEncryptor()
        self.multimodal = MultiModalProcessor()

    def generate_response(self, prompt: str) -> Generator:
        messages = self._prepare_messages(prompt)
        return ollama.chat(
            model=self.model_name,
            messages=messages,
            stream=True,
            options={
                'temperature': self.temperature,
                'num_ctx': self.config['model']['max_context']
            }
        )

    def _prepare_messages(self, prompt: str):
        """Prepare message history with context window management"""
        messages = [
            *self.history[-self.max_history:],
            {
                "role": "user", 
                "content": prompt,
                "images": [self.multimodal.process_image(img) for img in self.attachments]
            }
        ]

        return messages

    def add_to_history(self, prompt: str, response: str):
        """Manage conversation history with context window limits"""
        self.history.extend([
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": response}
        ])
        
        # Truncate history to maintain context window
        if len(self.history) > self.max_history * 2:
            self.history = self.history[-(self.max_history * 2):]

    def _process_attachments(self):
        return [self.multimodal.process_image(img) for img in self.attachments]

    def add_image(self, image_path: Path):
        self.attachments.append(image_path)

    def save_session(self):
        """Save encrypted conversation history"""
        encrypted = self.encryptor.encrypt_data(json.dumps({
            'history': self.history,
            'config': self.config
        }))
        session_file = Path(f"data/conversations/{int(time.time())}.enc")
        session_file.write_bytes(encrypted)