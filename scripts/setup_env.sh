#!/bin/bash

# Create directory structure
mkdir -p \
  local_ai/data/conversations/encrypted_chats \
  local_ai/data/models/{meta,blobs} \
  local_ai/data/config

# Generate default config with UI settings
cat << EOF > local_ai/data/config/settings.yaml
model:
  default: "llama3.2:latest"
  temperature: 0.7
  gpu_layers: 20
  max_context: 4096
  max_history: 6

privacy:
  encrypt_history: true

ui:
  theme: "dark"
  response_color: "cyan"
  prompt_symbol: "➤"
  show_thinking: true,
  assistant_prefix_color: "bold cyan"

EOF

# Set secure permissions
chmod 700 local_ai/data/
chmod 600 local_ai/data/config/settings.yaml

echo "Environment setup complete!"