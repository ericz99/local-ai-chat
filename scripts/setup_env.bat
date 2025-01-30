@echo off

mkdir local_ai\data\conversations\encrypted_chats
mkdir local_ai\data\models\meta
mkdir local_ai\data\models\blobs
mkdir local_ai\data\config

(
echo model:
echo   default: "llama3.2:latest"
echo   temperature: 0.7
echo   gpu_layers: 20
echo   max_context: 4096
echo   max_history: 6
echo 
echo privacy:
echo   encrypt_history: true
echo 
echo ui:
echo   theme: "dark"
echo   response_color: "cyan"
echo   prompt_symbol: "➤"
echo   show_thinking: true
echo   assistant_prefix_color: "bold cyan"
) > local_ai\data\config\settings.yaml

echo Environment setup complete!