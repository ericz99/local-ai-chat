import ollama
from rich.table import Table
from rich.console import Console
from pathlib import Path
import json

class ModelManager:
    def __init__(self):
        self.console = Console()
        self.models_dir = Path("data/models")
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
    def list_models(self):
        """List available and installed models"""
        local_models = ollama.list()['models']
        table = Table(title="Available Models")
        table.add_column("Name", style="cyan")
        table.add_column("Size", style="magenta")
        table.add_column("Digest", style="green")
        
        for model in local_models:
            table.add_row(model['name'], 
                         f"{model['size']/1e9:.1f} GB",
                         model['digest'][:12])
        
        self.console.print(table)
        
    def pull_model(self, model_name: str):
        """Download a model with progress tracking"""
        try:
            response = ollama.pull(model_name, stream=True)
            self.console.print(f"[yellow]Downloading {model_name}...[/yellow]")
            
            current_digest = ''
            for progress in response:
                if 'digest' in progress:
                    current_digest = progress['digest']
                if 'completed' in progress and 'total' in progress:
                    self.console.print(
                        f"Downloaded {progress['completed']/1e6:.1f}MB / "
                        f"{progress['total']/1e6:.1f}MB ({current_digest[:12]})"
                    )
        except Exception as e:
            self.console.print(f"[red]Download failed: {str(e)}[/red]")

    def delete_model(self, model_name: str):
        """Remove a local model"""
        try:
            ollama.delete(model_name)
            self.console.print(f"[green]Deleted {model_name} successfully![/green]")
        except Exception as e:
            self.console.print(f"[red]Deletion failed: {str(e)}[/red]")