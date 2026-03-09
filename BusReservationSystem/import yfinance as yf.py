import yfinance as yf
import sqlite3
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import re

# Database setup
conn = sqlite3.connect('portfolio.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS portfolio (
        symbol TEXT PRIMARY KEY,
        shares REAL
    )
''')
conn.commit()

def update_symbol_dropdown():
    c.execute("SELECT symbol FROM portfolio")
    symbols = [row[0] for row in c.fetchall()]
    symbol_dropdown['values'] = symbols

def fetch_price(symbol):
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="1d")
        if hist.empty:
            return None
        return hist['Close'].iloc[-1]
    except:
        return None

def is_valid_symbol(symbol):
    return re.fullmatch(r'^[A-Za-z0-9\.\-]+$', symbol) is not None

def add_stock(symbol, shares):
    symbol = symbol.strip().upper()
    try:
        shares = float(shares)
    except ValueError:
        shares = -1

    if not symbol or shares <= 0 or not is_valid_symbol(symbol):
        messagebox.showerror("Error", "Please enter a valid stock symbol and number of shares.")
        return

    price = fetch_price(symbol)
    if price is None:
        messagebox.showerror("Error", f"Could not fetch data for symbol '{symbol}'. Please check the symbol.")
        return

    c.execute("REPLACE INTO portfolio (symbol, shares) VALUES (?, ?)", (symbol, shares))
    conn.commit()
    messagebox.showinfo("Success", f"Added {shares} shares of {symbol}.")
    symbol_entry.delete(0, tk.END)
    shares_entry.delete(0, tk.END)
    update_symbol_dropdown()

def remove_stock():
    symbol = symbol_var.get()
    if not symbol:
        messagebox.showwarning("Warning", "Please select a stock symbol to remove.")
        return
    c.execute("DELETE FROM portfolio WHERE symbol=?", (symbol,))
    conn.commit()
    messagebox.showinfo("Removed", f"{symbol} removed from portfolio.")
    update_symbol_dropdown()

def show_portfolio():
    df = pd.read_sql_query("SELECT * FROM portfolio", conn)
    for row in tree.get_children():
        tree.delete(row)

    if df.empty:
        messagebox.showinfo("Info", "Your portfolio is empty.")
        total_label.config(text="Total Portfolio Value: $0.00")
        return

    total_value = 0
    df['Price'] = 0.0
    df['Value'] = 0.0

    for i, row in df.iterrows():
        price = fetch_price(row['symbol'])
        if price is not None:
            value = price * row['shares']
            df.at[i, 'Price'] = price
            df.at[i, 'Value'] = value
            total_value += value
        else:
            messagebox.showwarning("Warning", f"Skipping symbol {row['symbol']} due to price fetch failure.")

    for _, row in df.iterrows():
        tree.insert("", tk.END, values=(
            row['symbol'], row['shares'], f"${row['Price']:.2f}", f"${row['Value']:.2f}"
        ))

    total_label.config(text=f"Total Portfolio Value: ${total_value:.2f}")

# GUI
root = tk.Tk()
root.title("Stock Portfolio Tracker")
root.state('zoomed')

title = tk.Label(root, text="Stock Portfolio Tracker", font=("Helvetica", 20, "bold"), fg="#003366")
title.pack(pady=20)

frame_input = tk.Frame(root, pady=10)
frame_input.pack(fill='x', padx=30)

tk.Label(frame_input, text="Stock Symbol:", font=('Helvetica', 12)).grid(row=0, column=0, padx=10)
symbol_entry = tk.Entry(frame_input, font=('Helvetica', 12), width=20)
symbol_entry.grid(row=0, column=1, padx=10)

tk.Label(frame_input, text="Shares:", font=('Helvetica', 12)).grid(row=0, column=2, padx=10)
shares_entry = tk.Entry(frame_input, font=('Helvetica', 12), width=15)
shares_entry.grid(row=0, column=3, padx=10)

tk.Button(frame_input, text="Add Stock", command=lambda: add_stock(symbol_entry.get(), shares_entry.get())).grid(row=0, column=4, padx=10)

tk.Label(frame_input, text="Select to Remove:", font=('Helvetica', 12)).grid(row=1, column=0, padx=10)
symbol_var = tk.StringVar()
symbol_dropdown = ttk.Combobox(frame_input, textvariable=symbol_var, font=('Helvetica', 12), width=18)
symbol_dropdown.grid(row=1, column=1, padx=10)

tk.Button(frame_input, text="Remove Stock", command=remove_stock).grid(row=1, column=2, padx=10)
tk.Button(frame_input, text="Show Portfolio", command=show_portfolio).grid(row=1, column=3, padx=10)

# Table
frame_table = tk.Frame(root)
frame_table.pack(fill='both', expand=True, padx=30, pady=10)

columns = ("Symbol", "Shares", "Price", "Value")
tree = ttk.Treeview(frame_table, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor=tk.CENTER)

tree_scroll = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=tree_scroll.set)
tree.pack(side="left", fill="both", expand=True)
tree_scroll.pack(side="right", fill="y")

# Total
total_label = tk.Label(root, text="Total Portfolio Value: $0.00", font=('Helvetica', 14, "bold"), fg="green")
total_label.pack(pady=20)

update_symbol_dropdown()
root.mainloop()