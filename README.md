# Local Multi-Modal Chat CLI (LMCC)

A privacy-focused, locally-run chat interface supporting multi-modal interactions with AI models. Built with Python and Ollama.

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

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -e .

# Make script executable
chmod +x setup_env.sh

# Run setup
./scripts/setup_env.sh
```

## Usage

```bash
# Start chat session
local_mm_chat chat

# Chat with image
local_mm_chat chat --image path/to/image.png

# Chat with document
local_mm_chat chat --doc path/to/document.pdf

# Manage models
local_mm_chat model list
local_mm_chat model pull mistral:7b
local_mm_chat model delete llama2:13b
```

## Configuration

```bash
# dat/config/settings.yaml

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
