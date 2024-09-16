import tkinter as tk
from tkinter import ttk, messagebox
import sys
import subprocess
from connect_db import get_hotels_data, get_reviews_data

def show_booking_history(username):
    subprocess.run(["python", "history_booking.py", username])

def show_customer_support(username):
    subprocess.run(["python", "guest_support.py", username])

def user_interface(username):
    root = tk.Tk()
    root.title("Hotel Booking System")
    root.geometry("1200x800")
    root.configure(bg="#EAEAEA")

    header_frame = tk.Frame(root, bg="#2C3E50", padx=20, pady=10)
    header_frame.pack(fill="x", side="top")
    
    user_label = tk.Label(header_frame, text=f"Welcome, {username}", font=("Helvetica", 18, "bold"), fg="#ECF0F1", bg="#2C3E50")
    user_label.pack(anchor="w")

    main_frame = tk.Frame(root, bg="#EAEAEA")
    main_frame.pack(expand=1, fill="both", padx=20, pady=20)

    left_frame = tk.Frame(main_frame, bg="#FFFFFF", padx=10, pady=10, relief="solid", borderwidth=1)
    left_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))

    ttk.Label(left_frame, text="Select Region:", font=("Helvetica", 12, "bold")).pack(pady=(10, 5), anchor="w")
    region_combobox = ttk.Combobox(left_frame, state="readonly", width=50)
    region_combobox.pack(pady=5)

    ttk.Label(left_frame, text="Select Hotel:", font=("Helvetica", 12, "bold")).pack(pady=(10, 5), anchor="w")
    hotel_combobox = ttk.Combobox(left_frame, state="readonly", width=50)
    hotel_combobox.pack(pady=5)

    ttk.Label(left_frame, text="Room Type, Price, and Availability:", font=("Helvetica", 12, "bold")).pack(pady=(10, 5), anchor="w")
    
    tree_frame = tk.Frame(left_frame)
    tree_frame.pack(pady=5, fill="both", expand=True)

    columns = ("room_type", "price", "available_rooms")
    rooms_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
    rooms_tree.heading("room_type", text="Room Type")
    rooms_tree.heading("price", text="Price")
    rooms_tree.heading("available_rooms", text="Available Rooms")
    rooms_tree.pack(expand=True, fill="both")

    review_frame = tk.Frame(left_frame, bg="#FFFFFF", padx=10, pady=10, relief="solid", borderwidth=1)
    review_frame.pack(side="bottom", fill="both", padx=10, pady=(10, 0))

    ttk.Label(review_frame, text="Hotel Reviews:", font=("Helvetica", 12, "bold")).pack(pady=(10, 5), anchor="w")

    review_tree = ttk.Treeview(review_frame, columns=("reviewer", "rating", "comment"), show="headings", selectmode="browse")
    review_tree.heading("reviewer", text="Reviewer")
    review_tree.heading("rating", text="Rating")
    review_tree.heading("comment", text="Comment")
    review_tree.pack(expand=True, fill="both")

    right_frame = tk.Frame(main_frame, bg="#FFFFFF", padx=10, pady=10, relief="solid", borderwidth=1)
    right_frame.pack(side="right", fill="both", expand=True)

    ttk.Label(right_frame, text="Select Room Type:", font=("Helvetica", 12, "bold")).pack(pady=(10, 5), anchor="w")
    room_type_combobox = ttk.Combobox(right_frame, state="readonly", width=30)
    room_type_combobox.pack(pady=5)

    ttk.Label(right_frame, text="Full name:", font=("Helvetica", 10)).pack(pady=(10, 5), anchor="w")
    full_name_entry = ttk.Entry(right_frame, width=30)
    full_name_entry.pack(pady=5)
    
    ttk.Label(right_frame, text="Check-in Date (YYYY-MM-DD):", font=("Helvetica", 10)).pack(pady=(10, 5), anchor="w")
    check_in_entry = ttk.Entry(right_frame, width=30)
    check_in_entry.pack(pady=5)

    ttk.Label(right_frame, text="Check-out Date (YYYY-MM-DD):", font=("Helvetica", 10)).pack(pady=(10, 5), anchor="w")
    check_out_entry = ttk.Entry(right_frame, width=30)
    check_out_entry.pack(pady=5)

    ttk.Label(right_frame, text="Number of Rooms:", font=("Helvetica", 10)).pack(pady=(10, 5), anchor="w")
    quantity_entry = ttk.Entry(right_frame, width=30)
    quantity_entry.pack(pady=5)

    ttk.Label(right_frame, text="Total Price:", font=("Helvetica", 12, "bold")).pack(pady=(10, 5), anchor="w")
    total_price_label = ttk.Label(right_frame, text="$0.00", font=("Helvetica", 12, "bold"))
    total_price_label.pack(pady=5)

    def update_total_price():
        selected_room_type = room_type_combobox.get()
        quantity = quantity_entry.get()
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            total_price_label.config(text="$0.00")
            return

        if selected_room_type:
            region = region_combobox.get()
            hotel = hotel_combobox.get()
            if region in hotels_data and hotel in hotels_data[region]:
                price_per_room = hotels_data[region][hotel]["rooms"].get(selected_room_type, {}).get("price", 0)
                total_price = price_per_room * quantity
                total_price_label.config(text=f"${total_price:.2f}")

    book_button = ttk.Button(right_frame, text="Book Room", command=lambda: book_room(username, region_combobox.get(), hotel_combobox.get(), room_type_combobox.get(), check_in_entry.get(), check_out_entry.get(), quantity_entry.get()))
    book_button.pack(pady=20)

    link_frame = tk.Frame(right_frame, bg="#FFFFFF", padx=10, pady=10)
    link_frame.pack(side="bottom", fill="x")

    history_button = ttk.Button(link_frame, text="Booking History", command=lambda: show_booking_history(username))
    history_button.pack(side="left", padx=5)

    support_button = ttk.Button(link_frame, text="Customer Support", command=lambda: show_customer_support(username))
    support_button.pack(side="left", padx=5)

    def update_hotels():
        global hotels_data
        hotels_data = get_hotels_data()
        regions = sorted(set(data['region'] for data in hotels_data))
        region_combobox['values'] = regions
        if regions:
            region_combobox.current(0)
            update_hotels_data()
    
    def update_hotels_data():
        selected_region = region_combobox.get()
        hotels = [data['hotel_name'] for data in hotels_data if data['region'] == selected_region]
        hotel_combobox['values'] = hotels
        if hotels:
            hotel_combobox.current(0)
            update_rooms()

    def update_rooms():
        selected_region = region_combobox.get()
        selected_hotel = hotel_combobox.get()
        rooms_data = [data for data in hotels_data if data['region'] == selected_region and data['hotel_name'] == selected_hotel]
        rooms_tree.delete(*rooms_tree.get_children())
        review_tree.delete(*review_tree.get_children())
        room_type_combobox['values'] = []
        if rooms_data:
            for data in rooms_data:
                rooms_tree.insert("", "end", values=(data['room_type'], data['price'], data['available_rooms']))
                room_type_combobox['values'] = list(set(data['room_type'] for data in rooms_data))
            reviews_data = get_reviews_data()
            for review in reviews_data:
                if review['region'] == selected_region and review['hotel_name'] == selected_hotel:
                    review_tree.insert("", "end", values=(review['reviewer'], review['rating'], review['comment']))

    region_combobox.bind("<<ComboboxSelected>>", lambda e: update_hotels_data())
    hotel_combobox.bind("<<ComboboxSelected>>", lambda e: update_rooms())
    room_type_combobox.bind("<KeyRelease>", lambda e: update_total_price())
    quantity_entry.bind("<KeyRelease>", lambda e: update_total_price())

    def book_room(username, region, hotel, room_type, check_in, check_out, quantity):
        if not room_type or not check_in or not check_out or not quantity:
            messagebox.showwarning("Error", "Please fill in all the fields!")
            return

        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Error", "The number of rooms must be a positive integer!")
            return

        # Perform booking action (link to database here)
        messagebox.showinfo("Booking", f"{username} successfully booked {quantity} {room_type}(s) at {hotel} in {region} from {check_in} to {check_out}!")

    update_hotels()

    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        username = "Guest"
    
    user_interface(username)
