import typer
import csv
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text


app = typer.Typer(rich_markup_mode="rich")
console = Console()
DATA_FILE = "data.csv"

def print_header():
    """Prints a professional branded header."""
    header_text = Text("AMAZON FRESH | INVENTORY MANAGEMENT SYSTEM | UMA4", style="bold white")
    console.print(Panel(header_text, style="bold blue", expand=False))

def load_data():
    """Loads inventory from the CSV file."""
    if not os.path.exists(DATA_FILE):
        return [
            {"id": "1", "name": "Silk Soy Milk", "quantity": "12", "status": "active"},
            {"id": "2", "name": "Chobani Yogurt", "quantity": "24", "status": "active"},
            {"id": "3", "name": "Amazon Fresh Water 24pk", "quantity": "50", "status": "active"},
        ]
    with open(DATA_FILE, mode="r") as f:
        return list(csv.DictReader(f))

def save_data(inventory):
    """Saves the inventory list to the CSV file."""
    with open(DATA_FILE, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "quantity", "status"])
        writer.writeheader()
        writer.writerows(inventory)
        console.print(f"[italic cyan]📦 System Audit: {len(inventory)} items persisted to {DATA_FILE}[/]")

@app.command()
def list_stock():
    """Lists all items in the inventory with visuals"""
    print_header()
    inventory = load_data()
    
    table = Table(title="Live Warehouse Inventory", box=None, header_style="bold magenta")
    table.add_column("ID", justify="center", style="cyan")
    table.add_column("Product Name")
    table.add_column("Quantity", justify="right")
    table.add_column("Status", justify="center")

    for item in inventory:
        qty = int(item["quantity"])
        
        
        if item["status"].lower() == "damaged":
            color = "bold yellow"
        elif qty < 25:
            color = "bold red"
        else:
            color = "green"
            
        table.add_row(item["id"], item["name"], str(qty), item["status"].upper(), style=color)
    
    console.print(table)
    console.print(f"\n[bold blue]Total unique SKUs:[/] {len(inventory)}")

@app.command()
def add_item(name: str, qty: int):
    """Adds a new item to the inventory."""
    inventory = load_data()
    new_id = str(len(inventory) + 1)
    inventory.append({
        "id": new_id, 
        "name": name, 
        "quantity": str(qty),
        "status": "active"
    })
    save_data(inventory)
    console.print(f"[bold green]✅ Success![/] Added {name} to the system.")

@app.command()
def update_qty(item_id: str, change: int):
    """
    Adjusts stock. Use positive for Stow, negative for Pick.
    Example: update-qty -- 1 -5
    """
    inventory = load_data()
    found = False

    for item in inventory:
        if item["id"] == item_id:
            current_qty = int(item["quantity"])
            new_qty = current_qty + change
            
            if new_qty < 0:
                console.print(f"[bold red]❌ Error:[/] Insufficient stock. Current: {current_qty}")
                return
            
            item["quantity"] = str(new_qty)
            found = True
            break

    if found:
        save_data(inventory)
        console.print(f"[bold green]✅ Success![/] ID {item_id} updated to {item['quantity']}.")
    else:
        console.print(f"[bold red]❌ Error:[/] ID {item_id} not found.")

@app.command()
def mark_damage(item_id: str):
    """Flags an item as damaged for Problem Solve."""
    inventory = load_data()
    found = False

    for item in inventory:
        if item["id"] == item_id:
            item["status"] = "Damaged"
            found = True
            break
            
    if found:
        save_data(inventory)
        console.print(f"[bold yellow]⚠️ REPORTED:[/] Item {item_id} moved to DAMAGED status.")
    else:
        console.print(f"[bold red]❌ Error:[/] ID {item_id} not found.")

@app.command()
def del_item(item_id: str):
    """Removes an item from the system."""
    inventory = load_data()
    starting_count = len(inventory)
    inventory = [item for item in inventory if item["id"] != item_id]
    
    if len(inventory) == starting_count:
        console.print(f"[bold red]❌ Error:[/] ID {item_id} not found.")
    else:
        save_data(inventory)
        console.print(f"[bold green]🗑️ Success![/] Item ID {item_id} removed.")

@app.command()
def search(name: str):
    """Finds items by name."""
    inventory = load_data()
    results = [item for item in inventory if name.lower() in item['name'].lower()]

    if results:
        table = Table(title=f"results for '{name}'")
        table.add_column("ID", style="cyan")
        table.add_column("Product")
        table.add_column("Qty")
        for item in results:
            table.add_row(item["id"], item["name"], item["quantity"])
        console.print(table)
    else:
        console.print(f"[bold red]❌ No results found for '{name}'.[/]")

if __name__ == "__main__":
    app()