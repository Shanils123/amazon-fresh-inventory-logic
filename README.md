Amazon-Fresh (specially UMA4) Inventory Management System

![UMA4 Inventory System Demo](demo.gif)

This is a custom Command Line Interface (CLI) tool that I designed and created to simulate and streamline inventory workflow at Amazon Fresh Warehouse UMA4 in Boston. I built this project to practice data integrity, user input validation, and real time reporting using python.

Why I Built This

While currently working as a Warehouse Associate at an Amazon Fresh, I wanted to try fuse my studies of Computer Science with my work at Amazon. I also wanted to understand the logic behind our scanning and stowing systems. this tool manages the lifecycle of those products in the warehouse from when Recieving (Stow) to Problem Solve (Damage) to Outbound (Pick).

Core Features

Guided Workflows: So instead of memorizing ID numbers, this tool uses the "Search-first" logic. The user would have no problem finding a product, just find product by name and select the correct item from the search table.

Dual-inventory tracking: This tool tracks whether a product is Sellable or Damaged, keeping them separate to ensure inventory integrity.

Defensive Programming: Includes a robust 😏 error handling to prevent negative inventory, duplicate IDS, and invalid data types.

Rich UI: Experience color coded tables and branded headers using the Rich libray.

Tech Stack

Language: Python CLI Framework: Typer UI/Formatting: Rich Data Persistence: CSV

How to Run:

Clone repository
Install dependencies
How to Run
Bash

pip install typer rich

Run the application:
Bash

python main.py dashboard

python main.py --help

For The Future:

Expiry Track: Adding a "freshness" logic that flags the item when it's close to expiration.
