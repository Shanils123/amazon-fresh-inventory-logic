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
            {"id": "1", "name": "Silk Soy Milk 64oz", "qty_sellable": "45", "qty_damaged": "0", "status": "active"},
            {"id": "2", "name": "Chobani Greek Yogurt Strawberry", "qty_sellable": "8", "qty_damaged": "2", "status": "active"},
            {"id": "3", "name": "Organic Bananas (Bunch)", "qty_sellable": "120", "qty_damaged": "5", "status": "active"},
            {"id": "4", "name": "Amazon Fresh Water 24pk", "qty_sellable": "200", "qty_damaged": "0", "status": "active"},
            {"id": "5", "name": "Silk Almond Milk Vanilla", "qty_sellable": "15", "qty_damaged": "0", "status": "active"},
            {"id": "6", "name": "Whole Milk 1gal", "qty_sellable": "60", "qty_damaged": "3", "status": "active"},
            {"id": "7", "name": "Honeycrisp Apples 3lb Bag", "qty_sellable": "4", "qty_damaged": "0", "status": "active"},
            {"id": "8", "name": "Avocado 4ct Bag", "qty_sellable": "35", "qty_damaged": "1", "status": "active"},
        ]
    with open(DATA_FILE, mode="r") as f:
        return list(csv.DictReader(f))

def save_data(inventory):
    """Saves the inventory list to the CSV file."""
    with open(DATA_FILE, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "qty_sellable", "qty_damaged", "status"])
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
    table.add_column("Sellable", justify="right", style="green")
    table.add_column("Damaged", justify="right", style="red")
    table.add_column("Status", justify="center")

    for item in inventory:
        qty_sellable = int(item["qty_sellable"])
        qty_damaged = int(item["qty_damaged"])
        
        color = 'white'
        
        if item["status"].lower() == "damaged":
            color = "bold yellow"
        elif qty_sellable < 25:
            color = "bold red"
        else:
            color = "green"
            
        table.add_row(item["id"], item["name"], str(qty_sellable), str(qty_damaged), item["status"].upper(), style=color)
    
    console.print(table)
    console.print(f"\n[bold blue]Total unique SKUs:[/] {len(inventory)}")

@app.command()
def add_item(name: str, qty: int):
    """Adds a new item to the inventory."""
    inventory = load_data()
    
    if inventory:
        max_id = max(int(item["id"]) for item in inventory)
        new_id = str(max_id + 1)
    else:
        new_id = "1"
    
    inventory.append({
        "id": new_id, 
        "name": name, 
        "qty_sellable": str(qty),
        "qty_damaged": "0", 
        "status": "active"
    })
    
    save_data(inventory)
    console.print(f"[bold green]✅ Success![/] Added {name} with ID {new_id}.")

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
            current_qty = int(item["qty_sellable"])
            new_qty = current_qty + change
            
            if new_qty < 0:
                console.print(f"[bold red]❌ Error:[/] Insufficient stock. Current: {current_qty}")
                return
            
            item["qty_sellable"] = str(new_qty)
            found = True
            break

    if found:
        save_data(inventory)
        console.print(f"[bold green]✅ Success![/] ID {item_id} updated to {item['qty_sellable']}.")
    else:
        console.print(f"[bold red]❌ Error:[/] ID {item_id} not found.")

@app.command()
def mark_damage():
    """Problem Solve: search for an item and flag it as damaged."""
    print_header()
    inventory = load_data()

    searched_item = console.input("[bold yellow] Enter product name to report it as damaged: [/]")

    results = [item for item in inventory if searched_item.lower() in item['name'].lower()]

    if not results: 
        console.print(f"[bold red]❌ No results found for '{searched_item}'.[/]")
        return
    
    table = Table(title=f"results for '{searched_item}'")
    table.add_column("ID", style="cyan")
    table.add_column("Product Name")
    table.add_column("Current Qty")
    for item in results:
        table.add_row(item["id"], item["name"], f"S: {item['qty_sellable']} | D: {item['qty_damaged']}")
    console.print(table)

    target_id = console.input("[bold yellow] Enter the ID of the item to mark as damaged: [/]")

    damage_qty = int(console.input("[bold yellow] Enter quantity to mark as damaged: [/]"))

    if damage_qty <= 0:
        console.print("[bold red]❌ Error:[/] Please enter a positive number greater than 0.")
        return

    found = False
    for item in inventory:
        if item['id'] == target_id:
            current_s = int(item["qty_sellable"])
            current_d = int(item.get("qty_damaged"))

            if damage_qty > current_s:
                console.print(f"[bold red]❌ Error:[/] Cannot mark {damage_qty} as damaged. Only {current_s} sellable.")
                return
            
            item["qty_sellable"] = str(current_s - damage_qty)
            item["qty_damaged"] = str(current_d + damage_qty)
            found = True
            break
            
    if found:
        save_data(inventory)
        console.print(f"[bold yellow]⚠️ REPORTED:[/] Item {target_id} moved to DAMAGED status.")
    else:
        console.print(f"[bold red]❌ Error:[/] ID {target_id} not found.")

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
def pick():
    """Simulates a pick/ Searches for an ITEM and removes quantity from sellable stock."""
    print_header()
    inventory = load_data()

    search_term = console.input("[bold yellow] Enter product name to pick from: [/]")
    results = [item for item in inventory if search_term.lower() in item['name'].lower()]

    if not results:
        console.print(f"[bold red] ❌ No items found matching '{search_term}'.[/]")
        return
    
    table = Table(title=f"Select ID to pick from")
    table.add_column("ID", style="cyan")
    table.add_column("Product Name")
    table.add_column("sellable Qty", style="green")
    for item in results:
        table.add_row(item["id"], item["name"], item["qty_sellable"])
    console.print(table)

    target_id = console.input("[bold yellow] Enter the ID of the item to pick: [/]")

    try: 
        pick_qty = int(console.input("[bold yellow] How many are you picking? [/]"))
        if pick_qty <= 0:
            console.print("[bold red]❌ Error:[/] Please enter a positive number greater than 0.")
            return

    except ValueError:
        console.print("[bold red] ❌ Error:[/]  Quantity must be a number.")
        return


    found = False
    for item in inventory:
        if item['id'] == target_id:
            current_qty = int(item["qty_sellable"])
            if pick_qty > current_qty:
                console.print(f"[bold red]❌ Error:[/] Cannot pick {pick_qty}. Only {current_qty} available.")
                return
            item["qty_sellable"] = str(current_qty - pick_qty)
            found = True
            break

    if found:
        save_data(inventory)
        console.print(f"[bold green]✅ Success![/] Picked {pick_qty} of item {target_id}.")
    else:
        console.print(f"[bold red]❌ Error:[/] ID {target_id} not found.")


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
            table.add_row(item["id"], item["name"], f"S: {item['qty_sellable']} | D: {item['qty_damaged']}")
        console.print(table)
        console.print(f"\n[bold cyan] 🔍 Found {len(results)} matching items.[/]")
    else:
        console.print(f"[bold red]❌ No results found for '{name}'.[/]")

@app.command()
def dashboard():
    """📊 UMA4 Dashboard: warehouse health summary"""
    print_header()
    inventory = load_data()


    total_skus = len(inventory)
    total_sellable = sum(int(item["qty_sellable"]) for item in inventory)
    total_damaged = sum(int(item["qty_damaged"]) for item in inventory)
    low_stock_items = [item for item in inventory if int(item["qty_sellable"]) < 10]

    summary_text = (
        f"[bold blue]Total SKUs:[/] {total_skus}\n"
        f"[bold green]Total Sellable Items:[/] {total_sellable}\n"
        f"[bold red]Total Damaged Items:[/] {total_damaged}\n"
        f"[bold yellow]Low Stock Items (<10):[/] {len(low_stock_items)}"
    )
    
    console.print(Panel(summary_text, title="📊 Warehouse Dashboard", style="bold magenta"))

    if low_stock_items:
        table = Table(title="Critical Low Stock Items", box=None)
        table.add_column("Product", style="yellow")
        table.add_column("Qty", justify="right")
        for item in low_stock_items:
            table.add_row(item["name"], item["qty_sellable"])
        console.print(table)

if __name__ == "__main__":
    app()