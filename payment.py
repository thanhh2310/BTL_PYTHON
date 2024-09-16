import tkinter as tk
from tkinter import messagebox

def show_payment_window(room_type, number_of_rooms, total_price):
    def process_payment():
        # Hiển thị thông báo thanh toán thành công
        messagebox.showinfo("Success", "Thanh toán thành công!")
        payment_window.destroy()

    # Tạo cửa sổ thanh toán
    payment_window = tk.Tk()
    payment_window.title("Thanh toán")
    payment_window.geometry("400x300")
    payment_window.configure(bg="#F2F4F5")

    # Tiêu đề
    title_frame = tk.Frame(payment_window, bg="#007BFF", pady=20)
    title_frame.pack(fill="x")

    title_label = tk.Label(title_frame, text="Thông tin thanh toán", font=("Helvetica", 18, "bold"), fg="#FFFFFF", bg="#007BFF")
    title_label.pack()

    # Nội dung thanh toán
    content_frame = tk.Frame(payment_window, bg="#F2F4F5", padx=20, pady=20)
    content_frame.pack(expand=True, fill="both")

    # Thông tin thanh toán
    room_label = tk.Label(content_frame, text=f"Loại phòng:", font=("Helvetica", 14, "bold"), bg="#F2F4F5")
    room_label.grid(row=0, column=0, sticky="w", pady=5)
    room_value = tk.Label(content_frame, text=room_type, font=("Helvetica", 14), bg="#F2F4F5")
    room_value.grid(row=0, column=1, sticky="w", pady=5)

    number_label = tk.Label(content_frame, text=f"Số phòng đặt:", font=("Helvetica", 14, "bold"), bg="#F2F4F5")
    number_label.grid(row=1, column=0, sticky="w", pady=5)
    number_value = tk.Label(content_frame, text=number_of_rooms, font=("Helvetica", 14), bg="#F2F4F5")
    number_value.grid(row=1, column=1, sticky="w", pady=5)

    price_label = tk.Label(content_frame, text=f"Tổng tiền:", font=("Helvetica", 14, "bold"), bg="#F2F4F5")
    price_label.grid(row=2, column=0, sticky="w", pady=5)
    price_value = tk.Label(content_frame, text=f"${total_price}", font=("Helvetica", 14), bg="#F2F4F5")
    price_value.grid(row=2, column=1, sticky="w", pady=5)

    # Nút thanh toán
    payment_button = tk.Button(payment_window, text="Thanh toán", command=process_payment, bg="#28A745", fg="white", font=("Helvetica", 12, "bold"), relief="raised", padx=10, pady=5)
    payment_button.pack(pady=20)

    payment_window.mainloop()

# Ví dụ về cách sử dụng
show_payment_window("Single Room", 2, 100)
