import tkinter as tk
from tkinter import ttk, messagebox

from controllers.login_controller import LoginController


class LoginView:

    def __init__(self, root):
        self.root = root
        self.root.title("Gym Management System")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#f5f5f5")

        self.controller = LoginController()

        self.create_widgets()

    def create_widgets(self):

        title = tk.Label(
            self.root,
            text="GYM MANAGEMENT SYSTEM",
            font=("Arial", 20, "bold"),
            bg="#f5f5f5",
            fg="#0B5ED7"
        )
        title.pack(pady=25)

        frame = tk.Frame(
            self.root,
            bg="white",
            bd=2,
            relief="ridge"
        )
        frame.pack(padx=30, pady=10, fill="both", expand=True)

        tk.Label(
            frame,
            text="Admin Login",
            font=("Arial", 16, "bold"),
            bg="white"
        ).pack(pady=20)

        tk.Label(
            frame,
            text="Username",
            bg="white",
            anchor="w"
        ).pack(fill="x", padx=30)

        self.username_entry = ttk.Entry(frame, width=35)
        self.username_entry.pack(padx=30, pady=8)

        tk.Label(
            frame,
            text="Password",
            bg="white",
            anchor="w"
        ).pack(fill="x", padx=30)

        self.password_entry = ttk.Entry(
            frame,
            show="*",
            width=35
        )
        self.password_entry.pack(padx=30, pady=8)

        ttk.Button(
            frame,
            text="Login",
            command=self.login
        ).pack(pady=20)

        ttk.Button(
            frame,
            text="Clear",
            command=self.clear
        ).pack()

    def clear(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

    def login(self):

        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if username == "" or password == "":
            messagebox.showerror(
                "Error",
                "Please enter Username and Password."
            )
            return

        result = self.controller.login(username, password)

        if result:

            messagebox.showinfo(
                "Success",
                "Login Successful"
            )

            self.root.destroy()

            from tkinter import Tk
            from views.dashboard import Dashboard

            dashboard_root = Tk()
            Dashboard(dashboard_root)
            dashboard_root.mainloop()

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid Username or Password."
            )


if __name__ == "__main__":
    root = tk.Tk()
    LoginView(root)
    root.mainloop()