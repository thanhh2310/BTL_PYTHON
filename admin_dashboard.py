import tkinter as tk
import sys
from tkinter import ttk, messagebox, simpledialog

# Dữ liệu mẫu cho người dùng và đặt phòng
users_data = [
    {"username": "guest1", "role": "Guest"},
    {"username": "guest2", "role": "Guest"},
    {"username": "admin1", "role": "Admin"},
    {"username": "admin2", "role": "Admin"},
]

booking_data = [
    {"room": "Single Room", "hotel": "Hotel A", "status": "Booked", "price": 50, "region": "Region 1"},
    {"room": "Double Room", "hotel": "Hotel A", "status": "Pending", "price": 100, "region": "Region 1"},
    {"room": "Suite", "hotel": "Hotel C", "status": "Booked", "price": 300, "region": "Region 2"},
]

revenue_data = {
    "Room Stats": {"Single Room": 10, "Double Room": 7, "Suite": 3},
    "Region Revenue": {"Region 1": 1000, "Region 2": 800},
    "Hotel Revenue": {"Hotel A": 1200, "Hotel C": 600}
}

regions_data = []  # Dữ liệu khu vực
hotels_data = {}   # Dữ liệu khách sạn theo khu vực

# Giao diện trang Admin
def admin_interface(username):
    # Cửa sổ chính
    root = tk.Tk()
    root.title("Admin Dashboard")
    root.geometry("1200x800")
    root.configure(bg="#EAEAEA")

    # Khung tiêu đề
    header_frame = tk.Frame(root, bg="#2C3E50", padx=20, pady=10)
    header_frame.pack(fill="x", side="top")
    
    user_label = tk.Label(header_frame, text=f"Welcome, {username}", font=("Helvetica", 18, "bold"), fg="#ECF0F1", bg="#2C3E50")
    user_label.pack(anchor="w")

    title_label = tk.Label(header_frame, text="Admin Dashboard", font=("Helvetica", 24, "bold"), fg="#ECF0F1", bg="#2C3E50")
    title_label.pack(pady=10, anchor="center")

    # Tạo Tab
    tab_control = ttk.Notebook(root)

    # Tab Quản lý người dùng
    user_management_tab = ttk.Frame(tab_control)
    tab_control.add(user_management_tab, text="Quản lý người dùng")

    # Tab Quản lý đặt phòng
    booking_management_tab = ttk.Frame(tab_control)
    tab_control.add(booking_management_tab, text="Quản lý đặt phòng")

    # Tab Báo cáo doanh thu
    revenue_report_tab = ttk.Frame(tab_control)
    tab_control.add(revenue_report_tab, text="Báo cáo doanh thu")

    # Tab Quản lý khách sạn
    hotel_management_frame = ttk.Frame(tab_control)
    tab_control.add(hotel_management_frame, text="Quản lý khách sạn")

    tab_control.pack(expand=1, fill="both")

    # Giao diện Quản lý người dùng
    def refresh_user_treeview():
        for item in user_tree.get_children():
            user_tree.delete(item)
        for user in users_data:
            user_tree.insert("", "end", values=(user["username"], user["role"]))

    user_tree = ttk.Treeview(user_management_tab, columns=("username", "role"), show="headings")
    user_tree.heading("username", text="Username")
    user_tree.heading("role", text="Role")
    user_tree.pack(expand=True, fill="both", padx=10, pady=10)

    def delete_user():
        selected = user_tree.focus()
        if selected:
            values = user_tree.item(selected, "values")
            users_data[:] = [user for user in users_data if user["username"] != values[0]]
            refresh_user_treeview()
            messagebox.showinfo("Success", f"User {values[0]} deleted successfully!")
        else:
            messagebox.showwarning("Error", "Please select a user to delete!")

    def add_admin():
        users_data.append({"username": f"admin{len(users_data)+1}", "role": "Admin"})
        refresh_user_treeview()
        messagebox.showinfo("Success", "New admin added successfully!")

    delete_button = tk.Button(user_management_tab, text="Delete User", command=delete_user, bg="#C0392B", fg="white", font=("Helvetica", 12))
    delete_button.pack(side="left", padx=20, pady=10)

    add_admin_button = tk.Button(user_management_tab, text="Add Admin", command=add_admin, bg="#27AE60", fg="white", font=("Helvetica", 12))
    add_admin_button.pack(side="left", padx=20, pady=10)

    refresh_user_treeview()

    # Giao diện Quản lý đặt phòng
    def refresh_booking_treeview():
        for item in booking_tree.get_children():
            booking_tree.delete(item)
        for booking in booking_data:
            booking_tree.insert("", "end", values=(booking["room"], booking["hotel"], booking["status"], booking["price"]))

    booking_tree = ttk.Treeview(booking_management_tab, columns=("room", "hotel", "status", "price"), show="headings")
    booking_tree.heading("room", text="Room Type")
    booking_tree.heading("hotel", text="Hotel")
    booking_tree.heading("status", text="Status")
    booking_tree.heading("price", text="Price")
    booking_tree.pack(expand=True, fill="both", padx=10, pady=10)

    def cancel_booking():
        selected = booking_tree.focus()
        if selected:
            values = booking_tree.item(selected, "values")
            if values[2] == "Pending":
                booking_data[:] = [booking for booking in booking_data if booking["room"] != values[0]]
                refresh_booking_treeview()
                messagebox.showinfo("Success", f"Booking for {values[0]} has been cancelled!")
            else:
                messagebox.showwarning("Error", "Only pending bookings can be cancelled!")
        else:
            messagebox.showwarning("Error", "Please select a booking to cancel!")

    cancel_button = tk.Button(booking_management_tab, text="Cancel Booking", command=cancel_booking, bg="#C0392B", fg="white", font=("Helvetica", 12))
    cancel_button.pack(side="left", padx=20, pady=10)

    refresh_booking_treeview()

    # Giao diện Báo cáo doanh thu
    report_frame = tk.Frame(revenue_report_tab, padx=20, pady=20, bg="#EAEAEA")
    report_frame.pack(expand=True, fill="both")

    left_frame = tk.Frame(report_frame, bg="#ECF0F1", padx=10, pady=10)
    left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    middle_frame = tk.Frame(report_frame, bg="#ECF0F1", padx=10, pady=10)
    middle_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    right_frame = tk.Frame(report_frame, bg="#ECF0F1", padx=10, pady=10)
    right_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

    report_frame.grid_columnconfigure(0, weight=1)
    report_frame.grid_columnconfigure(1, weight=1)
    report_frame.grid_columnconfigure(2, weight=1)

    room_label = tk.Label(left_frame, text="Loại phòng được đặt nhiều nhất:", font=("Helvetica", 14), bg="#ECF0F1")
    room_label.pack(anchor="w")

    room_value = tk.Label(left_frame, text=max(revenue_data["Room Stats"], key=revenue_data["Room Stats"].get), font=("Helvetica", 14, "bold"), fg="#2C3E50", bg="#ECF0F1")
    room_value.pack(anchor="w")

    tk.Label(left_frame, text="Thống kê theo loại phòng:", font=("Helvetica", 12, "bold"), bg="#ECF0F1").pack(pady=10)
    room_tree = ttk.Treeview(left_frame, columns=("Room", "Bookings"), show="headings", height=5)
    room_tree.heading("Room", text="Room Type")
    room_tree.heading("Bookings", text="Number of Bookings")
    room_tree.pack(expand=True, fill="both")

    for room, count in revenue_data["Room Stats"].items():
        room_tree.insert("", "end", values=(room, count))

    tk.Label(middle_frame, text="Doanh thu theo khu vực:", font=("Helvetica", 14), bg="#ECF0F1").pack(anchor="w")

    region_tree = ttk.Treeview(middle_frame, columns=("Region", "Revenue"), show="headings", height=5)
    region_tree.heading("Region", text="Region")
    region_tree.heading("Revenue", text="Revenue")
    region_tree.pack(expand=True, fill="both")

    for region, revenue in revenue_data["Region Revenue"].items():
        region_tree.insert("", "end", values=(region, revenue))

    tk.Label(right_frame, text="Doanh thu theo khách sạn:", font=("Helvetica", 14), bg="#ECF0F1").pack(anchor="w")

    hotel_tree = ttk.Treeview(right_frame, columns=("Hotel", "Revenue"), show="headings", height=5)
    hotel_tree.heading("Hotel", text="Hotel")
    hotel_tree.heading("Revenue", text="Revenue")
    hotel_tree.pack(expand=True, fill="both")

    for hotel, revenue in revenue_data["Hotel Revenue"].items():
        hotel_tree.insert("", "end", values=(hotel, revenue))

    # Giao diện Quản lý khách sạn
    def refresh_hotel_treeview():
        for item in hotel_tree.get_children():
            hotel_tree.delete(item)
        for region, hotels in hotels_data.items():
            for hotel in hotels:
                for room_type, price in hotel["room_types"].items():
                    hotel_tree.insert("", "end", values=(region, hotel["name"], room_type, price, 1))  # Quantity set to 1 for simplicity

    def add_region():
        new_region = simpledialog.askstring("Add Region", "Enter new region name:")
        if new_region:
            if new_region not in regions_data:
                regions_data.append(new_region)
                region_combobox.config(values=regions_data)
                messagebox.showinfo("Success", f"Region '{new_region}' added successfully!")
            else:
                messagebox.showwarning("Error", "Region already exists!")
    
    def add_hotel():
        region = region_var.get()
        hotel_name = hotel_name_entry.get()
        room_type = room_type_entry.get()
        try:
            price = float(price_entry.get())
            quantity = int(quantity_entry.get())
        except ValueError:
            messagebox.showwarning("Error", "Price and Quantity must be valid numbers!")
            return
        
        if region and hotel_name and room_type and price is not None:
            if region in hotels_data:
                for hotel in hotels_data[region]:
                    if hotel["name"] == hotel_name:
                        hotel["room_types"][room_type] = price
                        refresh_hotel_treeview()
                        messagebox.showinfo("Success", f"Hotel '{hotel_name}' updated successfully!")
                        return
                # Add new hotel
                hotels_data[region].append({"name": hotel_name, "room_types": {room_type: price}})
                refresh_hotel_treeview()
                messagebox.showinfo("Success", f"Hotel '{hotel_name}' added successfully!")
            else:
                messagebox.showwarning("Error", "Invalid or non-existent region!")
        else:
            messagebox.showwarning("Error", "All fields must be filled!")

    def update_hotel():
        selected = hotel_tree.focus()
        if selected:
            values = hotel_tree.item(selected, "values")
            region = values[0]
            hotel_name = values[1]
            room_type = values[2]
            price = simpledialog.askfloat("Update Price", "Enter new price:")
            if price is not None:
                for hotel in hotels_data[region]:
                    if hotel["name"] == hotel_name:
                        hotel["room_types"][room_type] = price
                        refresh_hotel_treeview()
                        messagebox.showinfo("Success", f"Hotel '{hotel_name}' updated successfully!")
                        return
            else:
                messagebox.showwarning("Error", "Price update canceled!")
        else:
            messagebox.showwarning("Error", "Please select a hotel to update!")

    def delete_hotel():
        selected = hotel_tree.focus()
        if selected:
            values = hotel_tree.item(selected, "values")
            region = values[0]
            hotel_name = values[1]
            room_type = values[2]
            if region in hotels_data:
                for hotel in hotels_data[region]:
                    if hotel["name"] == hotel_name:
                        if room_type in hotel["room_types"]:
                            del hotel["room_types"][room_type]
                            if not hotel["room_types"]:
                                hotels_data[region].remove(hotel)
                            refresh_hotel_treeview()
                            messagebox.showinfo("Success", f"Hotel '{hotel_name}' deleted successfully!")
                            return
            else:
                messagebox.showwarning("Error", "Invalid region or hotel!")
        else:
            messagebox.showwarning("Error", "Please select a hotel to delete!")

    # UI Elements
    region_input_frame = tk.Frame(hotel_management_frame, padx=10, pady=10)
    region_input_frame.pack(fill="x", padx=10, pady=10)

    tk.Label(region_input_frame, text="Enter Region:", font=("Helvetica", 12)).pack(side="left", padx=5)
    region_var = tk.StringVar()
    region_combobox = ttk.Combobox(region_input_frame, textvariable=region_var, values=regions_data, font=("Helvetica", 12))
    region_combobox.pack(side="left", padx=5)
    
    tk.Label(region_input_frame, text="Hotel Name:", font=("Helvetica", 12)).pack(anchor="w", pady=5)
    hotel_name_entry = tk.Entry(region_input_frame, font=("Helvetica", 12))
    hotel_name_entry.pack(fill="x", pady=5)

    tk.Label(region_input_frame, text="Room Type:", font=("Helvetica", 12)).pack(anchor="w", pady=5)
    room_type_entry = tk.Entry(region_input_frame, font=("Helvetica", 12))
    room_type_entry.pack(fill="x", pady=5)

    tk.Label(region_input_frame, text="Price:", font=("Helvetica", 12)).pack(anchor="w", pady=5)
    price_entry = tk.Entry(region_input_frame, font=("Helvetica", 12))
    price_entry.pack(fill="x", pady=5)

    tk.Label(region_input_frame, text="Quantity:", font=("Helvetica", 12)).pack(anchor="w", pady=5)
    quantity_entry = tk.Entry(region_input_frame, font=("Helvetica", 12))
    quantity_entry.pack(fill="x", pady=5)

    add_hotel_button = tk.Button(region_input_frame, text="Add Hotel", command=add_hotel, bg="#4CAF50", fg="white", font=("Helvetica", 12))
    add_hotel_button.pack(side="left", padx=10, pady=10)
    
    add_hotel_button = tk.Button(region_input_frame, text="Add Region", command=add_region, bg="#4CAF50", fg="white", font=("Helvetica", 12))
    add_hotel_button.pack(side="left", padx=5)

    # Hotel Data Treeview
    tree_frame = tk.Frame(hotel_management_frame, padx=10, pady=10)
    tree_frame.pack(side="left", fill="both", expand=True)

    tk.Label(tree_frame, text="Hotel Data:", font=("Helvetica", 14)).pack(anchor="w", pady=5)
    hotel_tree = ttk.Treeview(tree_frame, columns=("region", "name", "room_type", "price", "quantity"), show="headings")
    hotel_tree.heading("region", text="Region")
    hotel_tree.heading("name", text="Hotel Name")
    hotel_tree.heading("room_type", text="Room Type")
    hotel_tree.heading("price", text="Price")
    hotel_tree.heading("quantity", text="Quantity")
    hotel_tree.pack(expand=True, fill="both")

    button_frame = tk.Frame(hotel_management_frame, padx=10, pady=10)
    button_frame.pack(side="right", fill="y")

    update_hotel_button = tk.Button(button_frame, text="Update Hotel", command=update_hotel, bg="#FF9800", fg="white", font=("Helvetica", 12), width=15)
    update_hotel_button.pack(side="top", padx=10, pady=5)

    delete_hotel_button = tk.Button(button_frame, text="Delete Hotel", command=delete_hotel, bg="#F44336", fg="white", font=("Helvetica", 12), width=15)
    delete_hotel_button.pack(side="top", padx=10, pady=5)

    refresh_hotel_treeview()
    root.mainloop()

# Gọi hàm admin_interface để chạy ứng dụng
if __name__ == "__main__":
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        username = "Guest"
    
    admin_interface(username)
