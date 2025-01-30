import typer
from pathlib import Path
from typing import Optional
from ..cli.interface import ChatInterface
from ..core.model_manager import ModelManager
from ..utils.error_handler import handle_errors

app = typer.Typer()

@app.command()
@handle_errors
def chat(
    image: Optional[Path] = typer.Option(None, "--image", help="Attach image file"),
    doc: Optional[Path] = typer.Option(None, "--doc", help="Attach document"),
):
    """Start a new chat session"""
    ChatInterface(
        image_path=image,
        document_path=doc,
    ).run()

@app.command()
@handle_errors
def model(
    action: str = typer.Argument(..., help="list/pull/delete"),
    name: Optional[str] = None
):
    """Manage local LLM models"""
    mm = ModelManager()
    
    # Handle actions differently
    if action == "list":
        if name:  # Validate no name for list
            raise typer.BadParameter("List action doesn't accept a model name")
        mm.list_models()
    elif action in ("pull", "delete"):
        if not name:
            raise typer.BadParameter(f"{action} requires a model name")
        getattr(mm, f"{action}_model")(name)
    else:
        raise typer.BadParameter("Invalid action")