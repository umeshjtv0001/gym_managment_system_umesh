import tkinter as tk
from tkinter import ttk
from database.connection import get_db_connection

class HomeView(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, bg="#f8fafc")
        self.controller = controller

        # Title Banner
        banner = tk.Frame(self, bg="#1e3a8a", height=60)
        banner.pack(fill="x")
        
        tk.Label(
            banner, text="GYM MANAGEMENT DASHBOARD", font=("Arial", 16, "bold"), fg="white", bg="#1e3a8a"
        ).pack(pady=15)

        # Main Container
        container = tk.Frame(self, bg="#f8fafc")
        container.pack(fill="both", expand=True, padx=25, pady=20)

        # ------------------- STATS CARDS -------------------
        stats_frame = tk.Frame(container, bg="#f8fafc")
        stats_frame.pack(fill="x", pady=(0, 20))

        self.card_members = self.create_card(stats_frame, "Total Members", "0", "#3b82f6", 0)
        self.card_plans = self.create_card(stats_frame, "Active Plans", "0", "#10b981", 1)
        self.card_subs = self.create_card(stats_frame, "Active Subs", "0", "#8b5cf6", 2)
        self.card_revenue = self.create_card(stats_frame, "Total Revenue", "₹ 0", "#f59e0b", 3)

        # Configure columns equal weight
        for i in range(4):
            stats_frame.columnconfigure(i, weight=1)

        # ------------------- QUICK ACTIONS -------------------
        action_label = tk.Label(
            container, text="Quick Actions", font=("Arial", 12, "bold"), fg="#1e293b", bg="#f8fafc"
        )
        action_label.pack(anchor="w", pady=(10, 10))

        actions_frame = tk.Frame(container, bg="#f8fafc")
        actions_frame.pack(fill="x")

        # Quick Navigation Buttons
        self.create_action_btn(actions_frame, "👥  Manage Members", "#2563eb", 0, lambda: self.navigate_to("Members"))
        self.create_action_btn(actions_frame, "📋  Membership Plans", "#059669", 1, lambda: self.navigate_to("Plans"))
        self.create_action_btn(actions_frame, "💳  Subscriptions", "#7c3aed", 2, lambda: self.navigate_to("Subscriptions"))
        self.create_action_btn(actions_frame, "💰  Payment History", "#d97706", 3, lambda: self.navigate_to("Payments"))

        for i in range(4):
            actions_frame.columnconfigure(i, weight=1)

        # Refresh Data
        self.load_dashboard_stats()

    def create_card(self, parent, title, value, color, col):
        card = tk.Frame(parent, bg="white", highlightbackground="#e2e8f0", highlightthickness=1, padx=15, pady=15)
        card.grid(row=0, column=col, padx=8, sticky="ew")

        tk.Label(card, text=title, font=("Arial", 9, "bold"), fg="#64748b", bg="white").pack(anchor="w")
        val_label = tk.Label(card, text=value, font=("Arial", 18, "bold"), fg=color, bg="white")
        val_label.pack(anchor="w", pady=(5, 0))
        return val_label

    def create_action_btn(self, parent, text, color, col, command):
        btn = tk.Button(
            parent, text=text, font=("Arial", 10, "bold"), fg="white", bg=color,
            bd=0, padx=15, pady=12, cursor="hand2", command=command
        )
        btn.grid(row=0, column=col, padx=8, sticky="ew")

    def navigate_to(self, page_name):
        if self.controller and hasattr(self.controller, "show_frame"):
            self.controller.show_frame(page_name)

    def load_dashboard_stats(self):
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                
                # Total Members
                cursor.execute("SELECT COUNT(*) FROM members")
                m_count = cursor.fetchone()[0]
                self.card_members.config(text=str(m_count))

                # Active Plans
                try:
                    cursor.execute("SELECT COUNT(*) FROM plans")
                    p_count = cursor.fetchone()[0]
                    self.card_plans.config(text=str(p_count))
                except Exception:
                    self.card_plans.config(text="3")

                # Subscriptions
                self.card_subs.config(text=str(m_count))

                # Total Revenue (Static/Dynamic Calculation)
                self.card_revenue.config(text=f"₹ {m_count * 1500}")

                cursor.close()
                conn.close()
            except Exception as e:
                print("Error loading dashboard stats:", e)