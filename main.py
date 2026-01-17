import typer
import csv
import os
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()
DATA_FILE = "data.csv"

def load_data():
    """Loads inventory from the CSV file."""
    if not os.path.exists(DATA_FILE):
        return [
            {"id": "1", "name": "Echo Dot", "quantity": "12"},
            {"id": "2", "name": "Kindle", "quantity": "4"},
        ]
    with open(DATA_FILE, mode="r") as f:
        return list(csv.DictReader(f))

def save_data(inventory):
    """Saves the inventory list to the CSV file."""
    with open(DATA_FILE, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "quantity"])
        writer.writeheader()
        writer.writerows(inventory)
        print(f"--- System Audit: {len(inventory)} items successfully persisted to {DATA_FILE} ---")

@app.command()
def list_stock():
    """Lists all items in the inventory."""
    inventory = load_data()
    table = Table(title="Live Warehouse Inventory")
    table.add_column("ID", style="cyan")
    table.add_column("Product Name", style="magenta")
    table.add_column("Quantity", style="green")

    for item in inventory:
        qty = int(item["quantity"])
        color = "red" if qty < 25 else "green"
        table.add_row(item["id"], item["name"], item["quantity"], style=color)
    console.print(table)

@app.command()
def add_item(name: str, qty: int):
    """Adds an item to the inventory."""
    inventory = load_data()
    new_id = str(len(inventory) + 1)
    inventory.append({"id": new_id, "name": name, "quantity": str(qty)})
    save_data(inventory)
    console.print(f"[bold green]Success![/bold green] Saved {name} to {DATA_FILE}")

@app.command()
def del_item(item_id: str):
    """Deletes an item from the inventory based on its ID."""
    inventory = load_data() # 1. Load the list from the file
    starting_count = len(inventory)
    
    # 2. Filter logic: Keep only items where the ID does NOT match the one to delete
    inventory = [item for item in inventory if item["id"] != item_id]
    
    # 3. Validation: Check if the length changed
    if len(inventory) == starting_count:
        console.print(f"[bold red]Error:[/] ID {item_id} not found in {DATA_FILE}")
    else:
        save_data(inventory) # 4. Save the new filtered list
        console.print(f"[bold green]Success![/] Item ID {item_id} removed from system.")

if __name__ == "__main__":
    app()