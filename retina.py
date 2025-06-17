import csv
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import main

CSV_FILE = "users.csv"

# Ensure CSV file exists
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["username", "email", "password"])

# Function to check user existence
def user_exists(username):
    with open(CSV_FILE, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == username:
                return row
    return None

# Function to handle signup
def signup():
    username = username_entry.get().strip()
    email = email_entry.get().strip()
    password = password_entry.get().strip()

    if not username or not email or not password:
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    users = []
    updated = False

    with open(CSV_FILE, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == username:
                row[1] = email
                row[2] = password
                updated = True
            users.append(row)

    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(users)

    if updated:
        messagebox.showinfo("Updated", "User details updated successfully!")
    else:
        with open(CSV_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([username, email, password])
        messagebox.showinfo("Success", "Signup successful!")
    
    clear_entries()

# Function to handle login
def login():
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if not username or not password:
        messagebox.showwarning("Input Error", "Username and password are required!")
        return

    user = user_exists(username)

    if user and user[2] == password:
        messagebox.showinfo("Success", "Login successful!")
        root.destroy()
        main.open_main()
    else:
        messagebox.showerror("Error", "Invalid username or password.")
        clear_entries()

# Function to clear input fields
def clear_entries():
    username_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

# Function to toggle password visibility
def toggle_password():
    if show_password_var.get():
        password_entry.config(show="")  # Show password
    else:
        password_entry.config(show="*")  # Hide password

# ---------------------- Tkinter GUI ----------------------
root = tk.Tk()
root.title("Login System for Diabetic retinopathy classification project")
root.geometry("800x500")

# Load background image
bg_image_path = "login_bg.png"

canvas = tk.Canvas(root, highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Function to update background dynamically
def update_background(event=None):
    if os.path.exists(bg_image_path):
        bg_image = Image.open(bg_image_path)
        bg_resized = bg_image.resize((root.winfo_width(), root.winfo_height()), Image.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_resized)
        canvas.create_image(0, 0, image=bg_photo, anchor="nw")
        canvas.bg_photo = bg_photo
    else:
        messagebox.showerror("Error", f"Background image not found: {bg_image_path}")

root.bind("<Configure>", update_background)

# Modern UI Frame
frame = tk.Frame(root, padx=40, pady=30, bg="white", relief="raised", borderwidth=3)
frame.place(relx=0.5, rely=0.5, anchor="center")

# Title
tk.Label(frame, text="Welcome Back!", font=("Arial", 18, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

# Labels & Entry Fields
tk.Label(frame, text="Username:", bg="white", font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
username_entry = tk.Entry(frame, width=35, font=("Arial", 12), relief="solid", borderwidth=1)
username_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame, text="Email:", bg="white", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=5)
email_entry = tk.Entry(frame, width=35, font=("Arial", 12), relief="solid", borderwidth=1)
email_entry.grid(row=2, column=1, padx=10, pady=5)

# Password Entry Field with Show Password Checkbox
tk.Label(frame, text="Password:", bg="white", font=("Arial", 12)).grid(row=3, column=0, sticky="w", pady=5)
password_entry = tk.Entry(frame, width=35, font=("Arial", 12), show="*", relief="solid", borderwidth=1)
password_entry.grid(row=3, column=1, padx=10, pady=5)

# Variable to track password visibility
show_password_var = tk.BooleanVar()

# Show Password Checkbox
show_password_check = tk.Checkbutton(frame, text="Show Password", variable=show_password_var, bg="white",
                                     font=("Arial", 10), command=toggle_password)
show_password_check.grid(row=4, column=1, sticky="w")

# Buttons
tk.Button(frame, text="Sign Up", command=signup, bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), relief="groove", width=15).grid(row=5, column=0, pady=15)
tk.Button(frame, text="Login", command=login, bg="#008CBA", fg="white", font=("Arial", 12, "bold"), relief="groove", width=15).grid(row=5, column=1, pady=15)

# Run the application
root.mainloop()
