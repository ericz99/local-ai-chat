import yaml 
from pathlib import Path
from typing import Dict, Any

DEFAULT_CONFIG = {
    'model': {
        'default': 'llama3.2:latest',
        'max_context': 4096,
        'max_history': 6,
        'temperature': 0.7
    },
    'privacy': {
        'encrypt_history': True
    },
    'ui': {
        'theme': 'dark',
        'response_color': 'magenta',
        'prompt_symbol': '➤',
        'show_thinking': True,
        'assistant_prefix_color': "bold cyan"
    }
}

def load_config() -> Dict[str, Any]:
    try:
        with open(Path("data/config/settings.yaml")) as f:
            user_config = yaml.safe_load(f) or {}
            return deep_update(DEFAULT_CONFIG, user_config)
    except FileNotFoundError:
        return DEFAULT_CONFIG
    

def deep_update(source, overrides):
    """Recursively update nested dictionaries"""
    for key, value in overrides.items():
        if isinstance(value, dict) and key in source:
            source[key] = deep_update(source.get(key, {}), value)
        else:
            source[key] = value
    return source