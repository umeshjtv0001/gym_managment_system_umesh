import tkinter as tk
from tkinter import ttk, messagebox

# Project Views Import
from views.memberview_view import MemberView
from views.plan_view import PlanView
from views.subscription_view import SubscriptionView
from views.payment_view import PaymentView
from views.user_view import UserView

class Dashboard(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Gym Management System - Dashboard")
        self.geometry("1100x650")
        self.configure(bg="#1e293b")

        # Layout Setup
        self.create_sidebar()
        self.create_main_content_area()

        # Default Screen
        self.show_home_view()

    def create_sidebar(self):
        self.sidebar = tk.Frame(self, bg="#0f172a", width=200)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        lbl_menu = tk.Label(
            self.sidebar, text="MENU", font=("Arial", 14, "bold"), bg="#0f172a", fg="white"
        )
        lbl_menu.pack(pady=(20, 20))

        btn_style = {
            "font": ("Arial", 11, "bold"),
            "bg": "#38bdf8",
            "fg": "white",
            "activebackground": "#0284c7",
            "activeforeground": "white",
            "bd": 0,
            "cursor": "hand2",
            "height": 2
        }

        buttons = [
            ("Home", self.show_home_view),
            ("Members", self.show_member_view),
            ("Plans", self.show_plan_view),
            ("Subscriptions", self.show_subscription_view),
            ("Payments", self.show_payment_view),
            ("Users", self.show_user_view)
        ]

        for text, command in buttons:
            btn = tk.Button(self.sidebar, text=text, command=command, **btn_style)
            btn.pack(fill="x", padx=10, pady=5)

        btn_logout = tk.Button(
            self.sidebar, text="Logout", command=self.logout, 
            font=("Arial", 11, "bold"), bg="#ef4444", fg="white", 
            activebackground="#dc2626", bd=0, cursor="hand2", height=2
        )
        btn_logout.pack(side="bottom", fill="x", padx=10, pady=20)

    def create_main_content_area(self):
        self.main_container = tk.Frame(self, bg="white")
        self.main_container.pack(side="right", expand=True, fill="both")

    def clear_main_container(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def render_view(self, ViewClass):
        self.clear_main_container()
        try:
            view_instance = ViewClass(self.main_container)
            if hasattr(view_instance, 'pack'):
                view_instance.pack(fill="both", expand=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load view: {e}")

    # Navigation Handlers
    def show_home_view(self):
        self.clear_main_container()
        header = tk.Frame(self.main_container, bg="#0369a1", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)

        lbl = tk.Label(header, text="GYM MANAGEMENT SYSTEM", font=("Arial", 18, "bold"), bg="#0369a1", fg="white")
        lbl.pack(expand=True)

        welcome = tk.Label(self.main_container, text="Welcome to Gym Management System", font=("Arial", 16), bg="white")
        welcome.pack(pady=100)

    def show_member_view(self):
        self.render_view(MemberView)

    def show_plan_view(self):
        self.render_view(PlanView)

    def show_subscription_view(self):
        self.render_view(SubscriptionView)

    def show_payment_view(self):
        self.render_view(PaymentView)

    def show_user_view(self):
        self.render_view(UserView)

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.destroy()