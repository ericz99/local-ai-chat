import time
from typing import Generator
from rich.live import Live
from rich.spinner import Spinner
from rich.console import Console

class StreamHandler:
    def __init__(self):
        self.console = Console()
        self.spinner = Spinner("dots", style="status.spinner")
        self.response = None
        
    def stream_response(self, response: Generator) -> str:
        full_response = []
        with Live(self.spinner, refresh_per_second=20) as live:
            start_time = time.time()
            try:
                for chunk in response:
                    token = chunk['message']['content']
                    full_response.append(token)
                    live.update(f"[cyan]{''.join(full_response)}[/cyan]")
                    
                    # Update spinner speed based on response rate
                    if time.time() - start_time > 1:
                        self.spinner.speed = 0.5
            except Exception as e:
                self.console.print(f"[red]Stream Error: {str(e)}[/red]")
                
        return ''.join(full_response)

    def display_progress(self, progress_type: str):
        """Show download/processing progress"""
        with self.console.status(f"[bold green]{progress_type}...") as status:
            while not self.complete:
                time.sleep(0.1)