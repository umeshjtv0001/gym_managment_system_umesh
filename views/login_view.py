import tkinter as tk
from tkinter import messagebox


class LoginView:

    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success
        self.root.title("Gym Management System - Login")
        self.root.geometry("400x450")
        self.root.configure(bg="#f4f6f7")
        self.root.resizable(False, False)

        # Title / Header
        header = tk.Frame(self.root, bg="#1f4e78", height=80)
        header.pack(fill="x")

        tk.Label(
            header,
            text="GYM MANAGEMENT",
            font=("Arial", 16, "bold"),
            bg="#1f4e78",
            fg="white"
        ).pack(pady=25)

        # Main Form Frame
        form_frame = tk.Frame(self.root, bg="#f4f6f7", padx=30, pady=20)
        form_frame.pack(fill="both", expand=True)

        tk.Label(
            form_frame,
            text="User Login",
            font=("Arial", 16, "bold"),
            bg="#f4f6f7",
            fg="#2c3e50"
        ).pack(pady=(10, 20))

        # Username Field
        tk.Label(
            form_frame,
            text="Username",
            font=("Arial", 10, "bold"),
            bg="#f4f6f7",
            fg="#34495e"
        ).pack(anchor="w")

        self.username_entry = tk.Entry(
            form_frame,
            font=("Arial", 11),
            bd=1,
            relief="solid"
        )
        self.username_entry.pack(fill="x", pady=(5, 15), ipady=5)

        # Password Field
        tk.Label(
            form_frame,
            text="Password",
            font=("Arial", 10, "bold"),
            bg="#f4f6f7",
            fg="#34495e"
        ).pack(anchor="w")

        self.password_entry = tk.Entry(
            form_frame,
            font=("Arial", 11),
            show="*",
            bd=1,
            relief="solid"
        )
        self.password_entry.pack(fill="x", pady=(5, 20), ipady=5)

        # Login Button
        login_btn = tk.Button(
            form_frame,
            text="LOGIN",
            font=("Arial", 11, "bold"),
            bg="#3498db",
            fg="white",
            bd=0,
            cursor="hand2",
            command=self.handle_login
        )
        login_btn.pack(fill="x", ipady=8, pady=10)

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Warning", "Please enter both Username and Password!")
            return

        # Basic Check (Aap isko apne LoginController ya DB check se replace kar sakte hain)
        if username == "admin" and password == "admin":
            messagebox.showinfo("Success", "Login Successful!")
            self.on_login_success()
        else:
            messagebox.showerror("Error", "Invalid Username or Password!")


if __name__ == "__main__":
    root = tk.Tk()

    def dummy_success():
        print("Logged in successfully!")

    LoginView(root, dummy_success)
    root.mainloop()