from rich.console import Console
from rich.prompt import Prompt
from rich.style import Style  
from rich.theme import Theme
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
        
        self.engine = ChatEngine(
            model_name=self.config['model']['default'],
            temperature=temp,
            gpu_layers=self.config['model']['gpu_layers']
        )

        self.prompt_symbol = self.ui_config.get('prompt_symbol', '>')
        self.response_color = self.ui_config.get('response_color', 'cyan')
        self.show_thinking = self.ui_config.get('show_thinking', True)
        
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
                    f"[bold green]{self.prompt_symbol}[/bold green]",
                    style=self._get_input_style()
                )
                    
                if self.show_thinking:
                    with self.console.status("[bold yellow]Thinking...[/bold yellow]"):
                        response_stream = self.engine.generate_response(prompt)
                else:
                    response_stream = self.engine.generate_response(prompt)
                    
                full_response = self._display_response(response_stream)
                self.engine.add_to_history(prompt, full_response)
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Session saved. Exiting...[/yellow]")
                self.engine.save_session()
                break

    def _display_response(self, response_stream): 
        full_response = []

        for chunk in response_stream:
            token = chunk['message']['content']
            full_response.append(token)
            self.console.print(
                f"[{self.response_color}]{token}[/{self.response_color}]",
                end="", flush=True
            )

        self.console.print("\n")
        
        return ''.join(full_response)
    