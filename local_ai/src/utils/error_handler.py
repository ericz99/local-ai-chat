from rich.console import Console
from functools import wraps
import ollama

console = Console()

def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ollama.ResponseError as e:
            console.print(f"[red]Model Error: {e.error}[/red]")
        except KeyboardInterrupt:
            console.print("\n[yellow]Session cancelled by user[/yellow]")
        except Exception as e:
            console.print(f"[bold red]Critical Error: {str(e)}[/bold red]")
    return wrapper