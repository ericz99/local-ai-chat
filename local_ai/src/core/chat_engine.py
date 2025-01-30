from pathlib import Path
from typing import Generator, Optional
import ollama
from ..utils.data_privacy import DataEncryptor
from ..models.multimodal import MultiModalProcessor
import json
import time

class ChatEngine:
    def __init__(self, model_name="llava:latest", temperature=0.7, gpu_layers=20):
        self.model_name = model_name
        self.temperature = temperature
        self.gpu_layers = gpu_layers
        self.history = []
        self.encryptor = DataEncryptor()
        self.multimodal = MultiModalProcessor()
        
        ollama.show_os_logs = False
        ollama.set_gpu_layers(gpu_layers)

    def generate_response(self, prompt: str) -> Generator:
        messages = self._prepare_messages(prompt)
        return ollama.chat(
            model=self.model_name,
            messages=messages,
            stream=True,
            options={
                'temperature': self.temperature,
                'num_ctx': 4096
            }
        )

    def _prepare_messages(self, prompt: str):
        return [
            *self.history,
            {"role": "user", "content": prompt, "images": self._process_attachments()}
        ]

    def _process_attachments(self):
        return [self.multimodal.process_image(img) for img in self.attachments]

    def add_image(self, image_path: Path):
        self.attachments.append(image_path)

    def save_session(self):
        encrypted = self.encryptor.encrypt_data(json.dumps(self.history))
        session_file = Path(f"data/conversations/{int(time.time())}.enc")
        session_file.write_bytes(encrypted)

    def add_to_history(self, prompt: str, response: str):
        self.history.extend([
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": response}
        ])
        
        if len(self.history) > self.config['max_history']:
            self.history = self.history[-self.config['max_history']:]