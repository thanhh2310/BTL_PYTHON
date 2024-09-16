import tkinter as tk
from tkinter import ttk
import sys
from connect_db import get_booking_history_data

def purchase_history_interface(username):
    root = tk.Tk()
    root.title("Purchase History")
    root.geometry("1200x700")
    root.configure(bg="#EAEAEA")

    header_frame = tk.Frame(root, bg="#2C3E50", padx=20, pady=10)
    header_frame.pack(fill="x", side="top")
    
    user_label = tk.Label(header_frame, text=f"Welcome, {username}", font=("Helvetica", 18, "bold"), fg="#ECF0F1", bg="#2C3E50")
    user_label.pack(anchor="w")

    title_label = tk.Label(header_frame, text="Purchase History", font=("Helvetica", 24, "bold"), fg="#ECF0F1", bg="#2C3E50")
    title_label.pack(pady=10, anchor="center")

    main_frame = tk.Frame(root, bg="#FFFFFF", padx=20, pady=20, relief="solid", borderwidth=1)
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)

    tree_label = tk.Label(main_frame, text="Your Booking History", font=("Helvetica", 16, "bold"), bg="#FFFFFF", fg="#2C3E50")
    tree_label.pack(anchor="w", pady=(0, 10))

    columns = ("date", "hotel", "room", "total_price", "status")
    tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=10)

    tree.heading("date", text="Date")
    tree.heading("hotel", text="Hotel")
    tree.heading("room", text="Room Type")
    tree.heading("total_price", text="Total Price")
    tree.heading("status", text="Status")

    tree.column("date", width=120, anchor="center")
    tree.column("hotel", width=200, anchor="center")
    tree.column("room", width=150, anchor="center")
    tree.column("total_price", width=100, anchor="center")
    tree.column("status", width=120, anchor="center")

    booking_history_data = get_booking_history_data(username)
    for entry in booking_history_data:
        tree.insert("", "end", values=(entry["date"], entry["hotel"], entry["room"], entry["total_price"], entry["status"]))

    tree.pack(expand=True, fill="both", padx=10, pady=10)

    back_button = tk.Button(main_frame, text="Back to Dashboard", font=("Helvetica", 12), bg="#3A4A67", fg="white", command=root.destroy)
    back_button.pack(pady=20, anchor="e")

    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        username = "Guest"
    
    purchase_history_interface(username)
