#!/bin/bash

# Create directory structure
mkdir -p \
  local_ai/src/data/conversations/encrypted_chats \
  local_ai/src/data/models/{meta,blobs} \
  local_ai/src/data/config

# Generate default config with UI settings
cat << EOF > local_ai/src/data/config/settings.yaml
model:
  default: "llava:latest"
  temperature: 0.7
  gpu_layers: 20
  max_context: 4096

privacy:
  encrypt_history: true

ui:
  theme: "dark"
  response_color: "cyan"
  prompt_symbol: "➤"
  show_thinking: true
EOF

# Set secure permissions
chmod 700 local_ai/src/data/
chmod 600 local_ai/src/data/config/settings.yaml

echo "Environment setup complete!"