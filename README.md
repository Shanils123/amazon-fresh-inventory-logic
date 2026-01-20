# Amazon-Fresh (UMA4) Inventory Management System

![UMA4 Inventory System Demo](demo.gif)

This is a custom Command Line Interface (CLI) tool designed to simulate and streamline inventory workflows at the Amazon Fresh Warehouse (UMA4) in Boston. I built this project to practice data integrity, user input validation, and real-time reporting using Python.

## Why I Built This

While working as a Warehouse Associate at Amazon Fresh, I wanted to fuse my Computer Science studies with my daily work. I developed this tool to understand the logic behind scanning and stowing systems, managing the product lifecycle from **Receiving (Stow)** to **Problem Solve (Damage)** and **Outbound (Pick)**.

## Core Features

- **Guided Workflows:** Uses "Search-first" logic so users don't have to memorize ID numbers. Simply find a product by name and select it from the generated table.
- **Dual-Inventory Tracking:** Separately tracks Sellable and Damaged units to ensure total inventory integrity.
- **Defensive Programming:** Includes robust error handling to prevent negative inventory, duplicate IDs, and invalid data types.
- **Rich UI:** Features color-coded tables and branded headers using the `Rich` library for a professional terminal experience.

## Tech Stack

- **Language:** Python
- **CLI Framework:** Typer
- **UI/Formatting:** Rich
- **Data Persistence:** CSV

## How to Run

1. **Clone the repository** to your local machine.
2. **Install dependencies**:
   `pip install typer rich`
   `python main.py dashboard`
   `python main.py --help`
