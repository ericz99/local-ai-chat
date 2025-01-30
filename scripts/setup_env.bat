@echo off

mkdir local_ai\src\data\conversations\encrypted_chats
mkdir local_ai\src\data\models\meta
mkdir local_ai\src\data\models\blobs
mkdir local_ai\src\data\config

(
echo model:
echo   default: "llava:latest"
echo   temperature: 0.7
echo   gpu_layers: 20
echo   max_context: 4096
echo 
echo privacy:
echo   encrypt_history: true
echo 
echo ui:
echo   theme: "dark"
echo   response_color: "cyan"
echo   prompt_symbol: "➤"
echo   show_thinking: true
) > local_ai\src\data\config\settings.yaml

echo Environment setup complete!