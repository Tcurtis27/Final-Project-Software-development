import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database setup
def init_db():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS inventory (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        category TEXT,
                        quantity INTEGER NOT NULL,
                        price REAL NOT NULL,
                        supplier TEXT)''')
    conn.commit()
    conn.close()

# Function to add an item
def add_item():
    name = entry_name.get()
    category = entry_category.get()
    quantity = entry_quantity.get()
    price = entry_price.get()
    supplier = entry_supplier.get()
    
    if not name or not quantity or not price:
        messagebox.showerror("Input Error", "Please enter required fields.")
        return
    
    try:
        quantity = int(quantity)
        price = float(price)
    except ValueError:
        messagebox.showerror("Input Error", "Quantity must be an integer and Price must be a number.")
        return
    
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO inventory (name, category, quantity, price, supplier) VALUES (?, ?, ?, ?, ?)", 
                   (name, category, quantity, price, supplier))
    conn.commit()
    conn.close()
    
    messagebox.showinfo("Success", "Item added successfully!")
    entry_name.delete(0, tk.END)
    entry_category.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_price.delete(0, tk.END)
    entry_supplier.delete(0, tk.END)

# Tkinter GUI setup
root = tk.Tk()
root.title("Inventory Management System")
root.geometry("400x400")

lbl_title = tk.Label(root, text="Add New Item", font=("Arial", 16))
lbl_title.pack(pady=10)

entry_name = tk.Entry(root, width=30)
entry_name.pack(pady=5)
entry_name.insert(0, "Item Name")

entry_category = tk.Entry(root, width=30)
entry_category.pack(pady=5)
entry_category.insert(0, "Category")

entry_quantity = tk.Entry(root, width=30)
entry_quantity.pack(pady=5)
entry_quantity.insert(0, "Quantity")

entry_price = tk.Entry(root, width=30)
entry_price.pack(pady=5)
entry_price.insert(0, "Price")

entry_supplier = tk.Entry(root, width=30)
entry_supplier.pack(pady=5)
entry_supplier.insert(0, "Supplier")

btn_add = tk.Button(root, text="Add Item", command=add_item)
btn_add.pack(pady=10)

init_db()
root.mainloop()
