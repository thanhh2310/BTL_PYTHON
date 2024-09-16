import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import subprocess

def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='123456',
            database='hotel_manager'
        )
        if connection.is_connected():
            print("Kết nối đến cơ sở dữ liệu thành công!")
    except Error as e:
        print(f"Lỗi khi kết nối cơ sở dữ liệu: {e}")
    return connection

def check_login(username, password):
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        connection.close()
        return user
def check_user(username, password):
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT user_type FROM Users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user_type = cursor.fetchone()
        connection.close()
        return user_type
        
def login():
    username = username_entry.get()
    password = password_entry.get()
    user = check_login(username, password)
    user_type = check_user(username, password)
    
    if user and user_type:
        if user_type['user_type'] == 'guest':
            # Open guest_dashboard.py and pass the username
            subprocess.run(["python", "guest_dashboard.py", username])
            login_screen.destroy()
        elif user_type['user_type'] == 'admin':
            # Open admin_dashboard.py and pass the username
            subprocess.run(["python", "admin_dashboard.py", username])
            login_screen.destroy()
    else:
        messagebox.showerror("Error", "Invalid username or password")

def login_screen():
    global login_screen
    login_screen = tk.Tk()
    login_screen.title("Login")
    login_screen.geometry("400x300")
    login_screen.config(bg="white")

    # Title
    tk.Label(login_screen, text="LOGIN", font=("Arial", 20, "bold"), bg="white", fg="#666").pack(pady=20)

    # Username label and entry
    tk.Label(login_screen, text="USERNAME", font=("Arial", 10, "bold"), bg="white", fg="#666").pack(anchor='w', padx=60)
    global username_entry
    username_entry = tk.Entry(login_screen, width=30, font=("Arial", 12), bd=0)
    username_entry.pack(pady=5)

    # Separator line for username
    username_sep = tk.Frame(login_screen, height=1, width=300, bg="#E0E0E0")
    username_sep.pack()

    # Password label and entry
    tk.Label(login_screen, text="PASSWORD", font=("Arial", 10, "bold"), bg="white", fg="#666").pack(anchor='w', padx=60)
    global password_entry
    password_entry = tk.Entry(login_screen, show="*", width=30, font=("Arial", 12), bd=0)
    password_entry.pack(pady=5)

    # Separator line for password
    password_sep = tk.Frame(login_screen, height=1, width=300, bg="#E0E0E0")
    password_sep.pack()

    # Forgot password link
    forgot_password = tk.Label(login_screen, text="FORGOT YOUR PASSWORD", font=("Arial", 10), bg="white", fg="#666")
    forgot_password.pack(pady=5)

    # Button frame for Register and Sign In
    button_frame = tk.Frame(login_screen, bg="white")
    button_frame.pack(side="bottom", fill="x")

    # Register button
    register_btn = tk.Button(button_frame, text="REGISTER", font=("Arial", 10, "bold"), bg="#F0F0F0", fg="#666", bd=0, width=15, command=register_screen)
    register_btn.pack(side="left", pady=20, padx=10)

    # Sign In button
    signin_btn = tk.Button(button_frame, text="SIGN IN", font=("Arial", 10, "bold"), bg="#3A4A67", fg="white", bd=0, width=15, command=login)
    signin_btn.pack(side="right", pady=20, padx=10)

    login_screen.mainloop()

def register_screen():
    register_screen = tk.Toplevel()
    register_screen.title("Register")
    register_screen.geometry("400x400")
    register_screen.config(bg="white")

    # Title
    tk.Label(register_screen, text="REGISTER", font=("Arial", 20, "bold"), bg="white", fg="#666").pack(pady=20)

    # Username label and entry
    tk.Label(register_screen, text="USERNAME", font=("Arial", 10, "bold"), bg="white", fg="#666").pack(anchor='w', padx=60)
    username_entry = tk.Entry(register_screen, width=30, font=("Arial", 12), bd=0)
    username_entry.pack(pady=5)

    # Separator line for username
    username_sep = tk.Frame(register_screen, height=1, width=300, bg="#E0E0E0")
    username_sep.pack()

    # Password label and entry
    tk.Label(register_screen, text="PASSWORD", font=("Arial", 10, "bold"), bg="white", fg="#666").pack(anchor='w', padx=60)
    password_entry = tk.Entry(register_screen, show="*", width=30, font=("Arial", 12), bd=0)
    password_entry.pack(pady=5)

    # Separator line for password
    password_sep = tk.Frame(register_screen, height=1, width=300, bg="#E0E0E0")
    password_sep.pack()

    # Email label and entry
    tk.Label(register_screen, text="EMAIL", font=("Arial", 10, "bold"), bg="white", fg="#666").pack(anchor='w', padx=60)
    email_entry = tk.Entry(register_screen, width=30, font=("Arial", 12), bd=0)
    email_entry.pack(pady=5)

    # Separator line for email
    email_sep = tk.Frame(register_screen, height=1, width=300, bg="#E0E0E0")
    email_sep.pack()

    # Phone label and entry
    tk.Label(register_screen, text="PHONE", font=("Arial", 10, "bold"), bg="white", fg="#666").pack(anchor='w', padx=60)
    phone_entry = tk.Entry(register_screen, width=30, font=("Arial", 12), bd=0)
    phone_entry.pack(pady=5)

    # Separator line for phone
    phone_sep = tk.Frame(register_screen, height=1, width=300, bg="#E0E0E0")
    phone_sep.pack()

    # User type (mặc định là guest, không hiển thị)
    user_type = "guest"

    # Register button
    register_btn = tk.Button(register_screen, text="REGISTER", font=("Arial", 10, "bold"), bg="#3A4A67", fg="white", bd=0, width=30)
    register_btn.pack(pady=20)

# Khởi chạy giao diện đăng nhập
login_screen()
