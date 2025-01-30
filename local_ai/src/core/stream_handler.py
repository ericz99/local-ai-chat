from rich.live import Live
from rich.console import Console
from rich.text import Text
from ..utils.config_loader import load_config

class StreamHandler:
    def __init__(self):
        self.config = load_config()
        self.console = Console()
        self.ui_config = self.config.get('ui', {})

        self.show_thinking = self.ui_config.get('show_thinking', True)
        self.response_color = self.ui_config.get('response_color', 'cyan')
        self.thinking_style = self.ui_config.get('thinking_style', 'yellow')
        self.assistant_prefix_color = self.ui_config.get('assistant_prefix_color', 'bold cyan')

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
    