from rich.console import Console
from rich.prompt import Prompt
from rich.style import Style  
from rich.theme import Theme
from rich.live import Live
from rich.text import Text
from ..core.stream_handler import StreamHandler
from ..core.chat_engine import ChatEngine
from ..utils.config_loader import load_config

class ChatInterface:
    def __init__(self, image_path=None, document_path=None, temp=0.7):
        self.stream_handler = StreamHandler()
        self.config = load_config()
        self.ui_config = self.config.get('ui', {})
        self.console = Console(
                style=self._get_theme_style(),
                theme=Theme({
                    "prompt": "bold green",
                    "response": self.ui_config.get('response_color', 'cyan')
                })
            )        
        
        self.engine = ChatEngine()

        self.prompt_symbol = self.ui_config.get('prompt_symbol', '>')
        self.response_color = self.ui_config.get('response_color', 'cyan')
        self.thinking_style = self.ui_config.get('thinking_style', 'yellow')
        self.show_thinking = self.ui_config.get('show_thinking', True)
        self.assistant_prefix_color = self.ui_config.get('assistant_prefix_color', 'bold cyan')
        
        self._show_welcome()
        self._handle_attachments(image_path, document_path)

    def _get_theme_style(self):
        theme = self.ui_config.get('theme', 'dark')
        return Style(
                color="white" if theme == "dark" else "black",
                bgcolor="black" if theme == "dark" else "white"
            )

    def _show_welcome(self):
        self.console.print(
            f"\n[bold blue]Local AI Chat[/bold blue] | Model: {self.engine.model_name} | "
            f"Temp: {self.engine.temperature}\n"
        )

    def _handle_attachments(self, image_path, document_path):
        if image_path:
            self.engine.add_image(image_path)
        if document_path:
            self.engine.add_document(document_path)

    def run(self):
        while True:
            try:
                prompt = Prompt.ask(
                    f"[bold green]{self.prompt_symbol}[/bold green]"
                )
            
                response_stream = self.engine.generate_response(prompt)
                full_response = self._display_response(response_stream)
                self.engine.add_to_history(prompt, full_response)
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Session saved. Exiting...[/yellow]")
                self.engine.save_session()
                break

    def _display_response(self, response_stream): 
        full_response = []
        response_display = Text("")

        if self.show_thinking:
            with Live(response_display, refresh_per_second=25, console=self.console) as live:
                # Show initial thinking indicator
                live.update(Text("[ASSISTANT]: Thinking...", style="yellow italic"))
                
                # Stream the actual response
                for chunk in response_stream:
                    token = chunk['message']['content']
                    full_response.append(token)
                    
                    # Build the updating response line
                    response_text = Text()
                    response_text.append("[ASSISTANT]: ", style=self.assistant_prefix_color)
                    response_text.append("".join(full_response))
                    
                    live.update(response_text)

        else:
            for chunk in response_stream:
                token = chunk['message']['content']
                full_response.append(token)
                self.console.print(
                    f"[{self.response_color}]{token}[/{self.response_color}]",
                    end=""
                )
        
        return ''.join(full_response)
    