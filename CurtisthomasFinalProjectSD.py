#Thomas Curtis
#3/7/2025
#software Devolpment

import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import json
import os
import csv
from datetime import datetime

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional Inventory Manager")
        self.root.geometry("800x600")
        self.inventory = []
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Professional theme

        # Create main window
        self.create_main_window()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Handle window close

    # Main window setup with menu bar and exit button
    def create_main_window(self):
        # Menu bar
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Inventory", command=self.clear_inventory, accelerator="Ctrl+N")
        file_menu.add_command(label="Save Inventory", command=self.open_save_window, accelerator="Ctrl+S")
        file_menu.add_command(label="Load Inventory", command=self.open_load_window, accelerator="Ctrl+L")
        file_menu.add_command(label="Export to CSV", command=self.export_to_csv, accelerator="Ctrl+E")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)

        action_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Actions", menu=action_menu)
        action_menu.add_command(label="Add Item", command=self.open_add_window, accelerator="Ctrl+A")
        action_menu.add_command(label="Edit Item", command=self.open_edit_window, accelerator="Ctrl+E")
        action_menu.add_command(label="Delete Item", command=self.delete_item, accelerator="Ctrl+D")
        action_menu.add_command(label="View Report", command=self.open_report_window)

        # Keyboard shortcuts
        self.root.bind("<Control-n>", lambda e: self.clear_inventory())
        self.root.bind("<Control-s>", lambda e: self.open_save_window())
        self.root.bind("<Control-l>", lambda e: self.open_load_window())
        self.root.bind("<Control-e>", lambda e: self.export_to_csv())
        self.root.bind("<Control-a>", lambda e: self.open_add_window())
        self.root.bind("<Control-e>", lambda e: self.open_edit_window())
        self.root.bind("<Control-d>", lambda e: self.delete_item())

        # Main content frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill="both", expand=True)

        ttk.Label(main_frame, text="Inventory Management System", font=("Arial", 16, "bold")).pack(pady=10)

        # Treeview for inventory display
        self.tree = ttk.Treeview(main_frame, columns=("Name", "Quantity", "Category"), show="headings", height=15)
        self.tree.heading("Name", text="Item Name")
        self.tree.heading("Quantity", text="Quantity")
        self.tree.heading("Category", text="Category")
        self.tree.column("Name", width=250)
        self.tree.column("Quantity", width=100)
        self.tree.column("Category", width=200)
        self.tree.pack(fill="both", expand=True, pady=10)

        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Buttons frame
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Add Item", command=self.open_add_window).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Edit Item", command=self.open_edit_window).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Delete Item", command=self.delete_item).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="View Report", command=self.open_report_window).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Exit", command=self.on_closing).pack(side="left", padx=5)  # Added Exit button

        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief="sunken", anchor="w")
        status_bar.pack(side="bottom", fill="x", pady=5)

    # Validate input fields
    def validate_input(self, name, quantity, category):
        if not all([name, quantity, category]):
            return False, "All fields are required."
        if not name.isalpha() or not category.isalpha():
            return False, "Name and category must be alphabetic."
        try:
            qty = int(quantity)
            if qty <= 0:
                return False, "Quantity must be positive."
        except ValueError:
            return False, "Quantity must be a number."
        return True, ""

    # Update Treeview
    def update_treeview(self):
        self.tree.delete(*self.tree.get_children())
        for item in self.inventory:
            self.tree.insert("", "end", values=(item["name"], item["quantity"], item["category"]))

    # Add item window
    def open_add_window(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add New Item")
        add_window.geometry("300x250")
        add_window.transient(self.root)
        add_window.grab_set()

        frame = ttk.Frame(add_window, padding="10")
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Add Item", font=("Arial", 12, "bold")).pack(pady=10)
        ttk.Label(frame, text="Name:").pack()
        name_entry = ttk.Entry(frame)
        name_entry.pack(pady=5)
        ttk.Label(frame, text="Quantity:").pack()
        qty_entry = ttk.Entry(frame)
        qty_entry.pack(pady=5)
        ttk.Label(frame, text="Category:").pack()
        cat_entry = ttk.Entry(frame)
        cat_entry.pack(pady=5)

        def add():
            name, qty, cat = name_entry.get().strip(), qty_entry.get().strip(), cat_entry.get().strip()
            is_valid, msg = self.validate_input(name, qty, cat)
            if is_valid:
                self.inventory.append({"name": name, "quantity": int(qty), "category": cat})
                self.update_treeview()
                self.status_var.set(f"Added {name} to inventory.")
                add_window.destroy()
            else:
                messagebox.showerror("Error", msg)

        ttk.Button(frame, text="Add", command=add).pack(pady=10)

    # Edit item window
    def open_edit_window(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select an item to edit.")
            return

        item_index = self.tree.index(selected[0])
        item = self.inventory[item_index]

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Item")
        edit_window.geometry("300x250")
        edit_window.transient(self.root)
        edit_window.grab_set()

        frame = ttk.Frame(edit_window, padding="10")
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Edit Item", font=("Arial", 12, "bold")).pack(pady=10)
        ttk.Label(frame, text="Name:").pack()
        name_entry = ttk.Entry(frame)
        name_entry.insert(0, item["name"])
        name_entry.pack(pady=5)
        ttk.Label(frame, text="Quantity:").pack()
        qty_entry = ttk.Entry(frame)
        qty_entry.insert(0, item["quantity"])
        qty_entry.pack(pady=5)
        ttk.Label(frame, text="Category:").pack()
        cat_entry = ttk.Entry(frame)
        cat_entry.insert(0, item["category"])
        cat_entry.pack(pady=5)

        def save():
            name, qty, cat = name_entry.get().strip(), qty_entry.get().strip(), cat_entry.get().strip()
            is_valid, msg = self.validate_input(name, qty, cat)
            if is_valid:
                self.inventory[item_index] = {"name": name, "quantity": int(qty), "category": cat}
                self.update_treeview()
                self.status_var.set(f"Edited {name} successfully.")
                edit_window.destroy()
            else:
                messagebox.showerror("Error", msg)

        ttk.Button(frame, text="Save", command=save).pack(pady=10)

    # Delete item
    def delete_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select an item to delete.")
            return
        item_index = self.tree.index(selected[0])
        name = self.inventory[item_index]["name"]
        del self.inventory[item_index]
        self.update_treeview()
        self.status_var.set(f"Deleted {name} from inventory.")

    # Report window with statistics
    def open_report_window(self):
        report_window = tk.Toplevel(self.root)
        report_window.title("Inventory Report")
        report_window.geometry("500x400")
        report_window.transient(self.root)
        report_window.grab_set()

        frame = ttk.Frame(report_window, padding="10")
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Inventory Report", font=("Arial", 14, "bold")).pack(pady=10)
        
        total_items = len(self.inventory)
        total_qty = sum(item["quantity"] for item in self.inventory)
        categories = len(set(item["category"] for item in self.inventory))

        ttk.Label(frame, text=f"Total Items: {total_items}").pack(pady=5)
        ttk.Label(frame, text=f"Total Quantity: {total_qty}").pack(pady=5)
        ttk.Label(frame, text=f"Unique Categories: {categories}").pack(pady=5)

        # Detailed list
        tree = ttk.Treeview(frame, columns=("Name", "Qty", "Cat"), show="headings", height=10)
        tree.heading("Name", text="Name")
        tree.heading("Qty", text="Quantity")
        tree.heading("Cat", text="Category")
        tree.column("Name", width=150)
        tree.column("Qty", width=80)
        tree.column("Cat", width=120)
        for item in self.inventory:
            tree.insert("", "end", values=(item["name"], item["quantity"], item["category"]))
        tree.pack(fill="both", expand=True, pady=10)

        ttk.Button(frame, text="Close", command=report_window.destroy).pack(pady=10)

    # Save inventory window
    def open_save_window(self):
        save_window = tk.Toplevel(self.root)
        save_window.title("Save Inventory")
        save_window.geometry("400x200")
        save_window.transient(self.root)
        save_window.grab_set()

        frame = ttk.Frame(save_window, padding="10")
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Save Inventory", font=("Arial", 12, "bold")).pack(pady=10)
        ttk.Label(frame, text="File Name:").pack()
        filename_entry = ttk.Entry(frame)
        default_name = f"inventory_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filename_entry.insert(0, default_name)
        filename_entry.pack(pady=5)

        def save():
            filename = filename_entry.get().strip()
            if not filename.endswith(".json"):
                filename += ".json"
            try:
                with open(filename, "w") as f:
                    json.dump(self.inventory, f, indent=4)
                self.status_var.set(f"Saved to {filename}.")
                save_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Save failed: {e}")

        ttk.Button(frame, text="Save", command=save).pack(pady=10)
        ttk.Button(frame, text="Cancel", command=save_window.destroy).pack(pady=5)

    # Load inventory window
    def open_load_window(self):
        load_window = tk.Toplevel(self.root)
        load_window.title("Load Inventory")
        load_window.geometry("400x300")
        load_window.transient(self.root)
        load_window.grab_set()

        frame = ttk.Frame(load_window, padding="10")
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Load Inventory", font=("Arial", 12, "bold")).pack(pady=10)
        listbox = tk.Listbox(frame, height=10, width=50)
        listbox.pack(pady=10)

        json_files = [f for f in os.listdir() if f.endswith(".json")]
        if not json_files:
            listbox.insert("end", "No saved inventories found.")
        else:
            for file in json_files:
                listbox.insert("end", file)

        def load():
            selected = listbox.curselection()
            if not selected or "No saved" in listbox.get(selected[0]):
                messagebox.showwarning("Warning", "Select a valid file.")
                return
            filename = listbox.get(selected[0])
            try:
                with open(filename, "r") as f:
                    self.inventory = json.load(f)
                self.update_treeview()
                self.status_var.set(f"Loaded {filename}.")
                load_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Load failed: {e}")

        ttk.Button(frame, text="Load", command=load).pack(pady=5)
        ttk.Button(frame, text="Cancel", command=load_window.destroy).pack(pady=5)

    # Export to CSV
    def export_to_csv(self):
        if not self.inventory:
            messagebox.showwarning("Warning", "No inventory to export.")
            return
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            try:
                with open(filename, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Name", "Quantity", "Category"])
                    for item in self.inventory:
                        writer.writerow([item["name"], item["quantity"], item["category"]])
                self.status_var.set(f"Exported to {filename}.")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {e}")

    # Clear inventory
    def clear_inventory(self):
        if messagebox.askyesno("Confirm", "Clear current inventory?"):
            self.inventory.clear()
            self.update_treeview()
            self.status_var.set("Inventory cleared.")

    # Handle application closing
    def on_closing(self):
        if messagebox.askokcancel("Exit", "Do you want to save before exiting?"):
            self.open_save_window()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
