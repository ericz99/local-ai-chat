# Local Multi-Modal AI Chat

A privacy-focused, locally-run chat interface supporting multi-modal interactions with AI models. Built with Python and Ollama.

![Demo](https://www.loom.com/share/9407da8069134891b6a04be8dc8882e1)

## Features

- 🔒 **100% Local Execution** - No data leaves your machine
- 🖼️ **Multi-Modal Support** - Chat with images, documents, and text
- ⚡ **Real-time Streaming** - Typewriter-style responses
- 🧠 **Model Management** - Easily switch between local LLMs
- 🔄 **Context Aware** - Maintains conversation history
- 🛡️ **Encrypted History** - Secures chat sessions
- 🎨 **Rich CLI Interface** - Beautiful terminal formatting

## Installation

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.ai/) installed locally
- Supported models downloaded (e.g., `llava`, `mistral`)

```bash
# Clone repository
git clone https://github.com/ericz99/local-ai-chat.git
cd local-ai-chat

# Using Poetry
poetry shell

# Install packages
poetry install

# Run setup_env
sh scripts/setup_env.sh

# Run CLI
poetry run python main.py chat
```

## Configuration

```bash
# data/config/settings.yaml

model:
  default: "llava:latest"
  temperature: 0.7  # 0-1, creativity control
  gpu_layers: 20    # Use 0 for CPU-only
  max_history: 6    # Context window size

privacy:
  encrypt_history: true
  auto_clear_temp: true

ui:
  theme: "dark"     # dark/light
  response_color: "cyan"
```
