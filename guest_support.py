import tkinter as tk
from tkinter import ttk, messagebox
import sys

def customer_support_interface(username):
    # Cửa sổ chính
    root = tk.Tk()
    root.title("Customer Support")
    root.geometry("1200x700")
    root.configure(bg="#EAEAEA")

    # Khung tiêu đề
    header_frame = tk.Frame(root, bg="#2C3E50", padx=20, pady=10)
    header_frame.pack(fill="x", side="top")
    
    user_label = tk.Label(header_frame, text=f"Welcome, {username}", font=("Helvetica", 18, "bold"), fg="#ECF0F1", bg="#2C3E50")
    user_label.pack(anchor="w")

    title_label = tk.Label(header_frame, text="Customer Support", font=("Helvetica", 24, "bold"), fg="#ECF0F1", bg="#2C3E50")
    title_label.pack(pady=10, anchor="center")

    # Khung chính
    main_frame = tk.Frame(root, bg="#FFFFFF", padx=20, pady=20, relief="solid", borderwidth=1)
    main_frame.pack(expand=True, fill="both", padx=20, pady=20)

    # Nút Back to Dashboard ở trên "How to Contact Us"
    back_button = tk.Button(main_frame, text="Back to Dashboard", font=("Helvetica", 12), bg="#3A4A67", fg="white", command=root.destroy)
    back_button.pack(pady=(0, 20), anchor="w")

    # Phần thông tin liên hệ
    contact_frame = tk.Frame(main_frame, bg="#FFFFFF", padx=10, pady=10)
    contact_frame.pack(side="left", fill="both", expand=True)

    contact_label = tk.Label(contact_frame, text="How to Contact Us", font=("Helvetica", 16, "bold"), bg="#FFFFFF", fg="#2C3E50")
    contact_label.pack(pady=(10, 20), anchor="w")

    info_text = """For any inquiries or assistance, please feel free to contact us:
    
    - Phone: +1 (123) 456-7890
    - Email: support@hotelbooking.com
    - Live Chat: Available 24/7 via our website
    """
    contact_info_label = tk.Label(contact_frame, text=info_text, font=("Helvetica", 12), bg="#FFFFFF", fg="#34495E", justify="left")
    contact_info_label.pack(pady=10, anchor="w")

    # Phần mẫu yêu cầu hỗ trợ
    form_frame = tk.Frame(main_frame, bg="#FFFFFF", padx=10, pady=10)
    form_frame.pack(side="right", fill="both", expand=True)

    form_label = tk.Label(form_frame, text="Submit a Support Request", font=("Helvetica", 16, "bold"), bg="#FFFFFF", fg="#2C3E50")
    form_label.pack(pady=(10, 20), anchor="w")

    # Tạo form yêu cầu hỗ trợ
    ttk.Label(form_frame, text="Full Name:", font=("Helvetica", 12)).pack(pady=(10, 5), anchor="w")
    name_entry = ttk.Entry(form_frame, width=40)
    name_entry.pack(pady=5)

    ttk.Label(form_frame, text="Email Address:", font=("Helvetica", 12)).pack(pady=(10, 5), anchor="w")
    email_entry = ttk.Entry(form_frame, width=40)
    email_entry.pack(pady=5)

    ttk.Label(form_frame, text="Issue/Query:", font=("Helvetica", 12)).pack(pady=(10, 5), anchor="w")
    issue_combobox = ttk.Combobox(form_frame, values=["Booking Issues", "Payment Issues", "Room Availability", "Other"], state="readonly", width=37)
    issue_combobox.pack(pady=5)

    ttk.Label(form_frame, text="Message:", font=("Helvetica", 12)).pack(pady=(10, 5), anchor="w")
    message_textbox = tk.Text(form_frame, width=40, height=5)
    message_textbox.pack(pady=5)

    # Khu vực hiển thị câu hỏi và trả lời
    history_frame = tk.Frame(root, bg="#FFFFFF", padx=20, pady=20, relief="solid", borderwidth=1)
    history_frame.pack(expand=True, fill="both", padx=20, pady=20, side="bottom")

    history_label = tk.Label(history_frame, text="Chat History", font=("Helvetica", 16, "bold"), bg="#FFFFFF", fg="#2C3E50")
    history_label.pack(pady=(10, 10), anchor="w")

    history_text = tk.Text(history_frame, width=120, height=10, state="disabled", bg="#ECF0F1")
    history_text.pack(pady=5)

    # Cập nhật nội dung lịch sử
    def update_history(question, answer):
        history_text.config(state="normal")
        history_text.insert(tk.END, f"Question: {question}\nAnswer: {answer}\n\n")
        history_text.config(state="disabled")

    # Xử lý gửi yêu cầu
    def submit_request():
        name = name_entry.get()
        email = email_entry.get()
        issue = issue_combobox.get()
        message = message_textbox.get("1.0", tk.END).strip()

        if not name or not email or not issue or not message:
            tk.messagebox.showwarning("Error", "Please fill out all fields!")
        else:
            # Xử lý yêu cầu hỗ trợ (liên kết cơ sở dữ liệu hoặc gửi email ở đây)
            tk.messagebox.showinfo("Success", "Your support request has been submitted successfully!")
            # Xóa form sau khi gửi
            name_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)
            issue_combobox.set('')
            message_textbox.delete("1.0", tk.END)

            # Giả sử câu trả lời tự động cho câu hỏi
            automatic_reply = "Thank you for contacting us. Our team will respond to your query soon."
            update_history(message, automatic_reply)

    submit_button = tk.Button(form_frame, text="Submit Request", font=("Helvetica", 12), bg="#3A4A67", fg="white", command=submit_request)
    submit_button.pack(pady=20)

    root.mainloop()

# Khởi chạy giao diện với tên người dùng
if __name__ == "__main__":
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        username = "Guest"
    
    customer_support_interface(username)
