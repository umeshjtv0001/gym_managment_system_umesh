import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from database.connection import get_db_connection

class SubscriptionView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")

        # Title Header
        title_label = tk.Label(
            self, text="Subscription Management", font=("Arial", 16, "bold"), bg="white", fg="#1e3a8a"
        )
        title_label.pack(anchor="w", padx=20, pady=(15, 5))

        # ------------------- Form Controls Frame -------------------
        form_frame = tk.LabelFrame(self, text="Manage Subscription", font=("Arial", 10, "bold"), bg="white", padx=15, pady=10)
        form_frame.pack(fill="x", padx=20, pady=5)

        # Row 1: Member & Plan
        tk.Label(form_frame, text="Select Member:", bg="white", font=("Arial", 9)).grid(row=0, column=0, sticky="w", pady=5)
        self.combo_member = ttk.Combobox(form_frame, state="readonly", width=20)
        self.combo_member.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Plan:", bg="white", font=("Arial", 9)).grid(row=0, column=2, sticky="w", pady=5)
        self.combo_plan = ttk.Combobox(
            form_frame, 
            values=["Monthly Basic (30 Days)", "Quarterly Pro (90 Days)", "Yearly VIP (365 Days)"], 
            state="readonly", 
            width=22
        )
        self.combo_plan.current(0)
        self.combo_plan.grid(row=0, column=3, padx=10, pady=5)

        # Row 2: Start Date
        tk.Label(form_frame, text="Start Date (YYYY-MM-DD):", bg="white", font=("Arial", 9)).grid(row=1, column=0, sticky="w", pady=5)
        self.txt_start_date = tk.Entry(form_frame, width=23)
        self.txt_start_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.txt_start_date.grid(row=1, column=1, padx=10, pady=5)

        # Action Buttons (Add, Update, Delete, Clear)
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.grid(row=2, column=0, columnspan=4, pady=(10, 5), sticky="w")

        tk.Button(
            btn_frame, text="Add / Assign", bg="#22c55e", fg="white", 
            font=("Arial", 9, "bold"), bd=0, padx=12, pady=5, command=self.add_subscription
        ).pack(side="left", padx=4)

        tk.Button(
            btn_frame, text="Update Plan", bg="#3b82f6", fg="white", 
            font=("Arial", 9, "bold"), bd=0, padx=12, pady=5, command=self.update_subscription
        ).pack(side="left", padx=4)

        tk.Button(
            btn_frame, text="Delete", bg="#ef4444", fg="white", 
            font=("Arial", 9, "bold"), bd=0, padx=12, pady=5, command=self.delete_subscription
        ).pack(side="left", padx=4)

        tk.Button(
            btn_frame, text="Clear Form", bg="#6b7280", fg="white", 
            font=("Arial", 9, "bold"), bd=0, padx=12, pady=5, command=self.clear_form
        ).pack(side="left", padx=4)

        # ------------------- Search & Refresh Bar -------------------
        filter_frame = tk.Frame(self, bg="white")
        filter_frame.pack(fill="x", padx=20, pady=(10, 5))

        tk.Label(filter_frame, text="Search Member / Plan:", font=("Arial", 9, "bold"), bg="white").pack(side="left", padx=(0, 5))
        self.txt_search = tk.Entry(filter_frame, width=25)
        self.txt_search.pack(side="left", padx=5)
        self.txt_search.bind("<KeyRelease>", self.filter_subscriptions)

        # Refresh Button
        tk.Button(
            filter_frame, text="🔄 Refresh Data", bg="#0284c7", fg="white", 
            font=("Arial", 9, "bold"), bd=0, padx=12, pady=3, command=self.refresh_all
        ).pack(side="right", padx=5)

        # ------------------- Table Frame -------------------
        table_frame = tk.Frame(self, bg="white")
        table_frame.pack(fill="both", expand=True, padx=20, pady=(5, 15))

        columns = ("sub_id", "member_name", "plan", "start_date", "end_date", "status")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.table.heading("sub_id", text="Sub ID")
        self.table.heading("member_name", text="Member Name")
        self.table.heading("plan", text="Plan Name")
        self.table.heading("start_date", text="Start Date")
        self.table.heading("end_date", text="End Date")
        self.table.heading("status", text="Status")

        self.table.column("sub_id", width=60, anchor="center")
        self.table.column("member_name", width=150)
        self.table.column("plan", width=140)
        self.table.column("start_date", width=100, anchor="center")
        self.table.column("end_date", width=100, anchor="center")
        self.table.column("status", width=100, anchor="center")

        self.table.pack(fill="both", expand=True)

        # Click event to select row
        self.table.bind("<<TreeviewSelect>>", self.on_subscription_select)

        self.all_subscriptions = []
        self.selected_member_name = None

        # Initial Load
        self.refresh_all()

    # ------------------- Logic Functions -------------------

    def load_members_dropdown(self):
        """Database se members load karega dropdown me"""
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT name FROM members")
                members = cursor.fetchall()
                member_names = [m['name'] for m in members]
                self.combo_member['values'] = member_names
                if member_names:
                    self.combo_member.current(0)
                cursor.close()
                conn.close()
            except Exception as e:
                print("Error loading members for dropdown:", e)

    def load_subscriptions(self):
        """Subscriptions list load karta hai"""
        for row in self.table.get_children():
            self.table.delete(row)

        conn = get_db_connection()
        self.all_subscriptions = []
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM members")
                rows = cursor.fetchall()

                sub_id_counter = 101
                today = datetime.now().date()

                for r in rows:
                    m_name = r.get("name", "Unknown")
                    plan = r.get("plan", "Monthly Basic")
                    
                    start_dt = r.get("payment_date") or today.strftime("%Y-%m-%d")
                    try:
                        s_date = datetime.strptime(str(start_dt), "%Y-%m-%d").date()
                    except Exception:
                        s_date = today

                    days = 30
                    if "Quarterly" in str(plan):
                        days = 90
                    elif "Yearly" in str(plan):
                        days = 365

                    e_date = s_date + timedelta(days=days)
                    status = "Active" if e_date >= today else "Expired"

                    sub_data = (sub_id_counter, m_name, plan, str(s_date), str(e_date), status)
                    self.all_subscriptions.append(sub_data)
                    self.table.insert("", "end", values=sub_data)
                    sub_id_counter += 1

                cursor.close()
                conn.close()
            except Exception as e:
                print("Error loading subscriptions:", e)

    def filter_subscriptions(self, event=None):
        """Search query ke according filter karega"""
        query = self.txt_search.get().strip().lower()
        for row in self.table.get_children():
            self.table.delete(row)

        for sub in self.all_subscriptions:
            if query in str(sub[1]).lower() or query in str(sub[2]).lower():
                self.table.insert("", "end", values=sub)

    def add_subscription(self):
        """Add / Assign Subscription Action"""
        member = self.combo_member.get()
        plan = self.combo_plan.get().split(" (")[0]
        start_date = self.txt_start_date.get().strip()

        if not member:
            messagebox.showwarning("Warning", "Please select a member!")
            return

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE members SET plan=%s, payment_date=%s WHERE name=%s", (plan, start_date, member))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Success", f"Subscription assigned to {member} successfully!")
                self.refresh_all()
            except Exception as e:
                messagebox.showerror("Database Error", str(e))

    def update_subscription(self):
        """Update Plan Action"""
        if not self.selected_member_name:
            messagebox.showwarning("Selection Required", "Please select a subscription row from the table first!")
            return

        plan = self.combo_plan.get().split(" (")[0]
        start_date = self.txt_start_date.get().strip()

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE members SET plan=%s, payment_date=%s WHERE name=%s", (plan, start_date, self.selected_member_name))
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("Success", f"Subscription updated for {self.selected_member_name}!")
                self.refresh_all()
            except Exception as e:
                messagebox.showerror("Database Error", str(e))

    def delete_subscription(self):
        """Delete Subscription Action"""
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select a subscription to delete!")
            return

        row = self.table.item(selected[0])['values']
        member_name = row[1]

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to remove subscription for {member_name}?"):
            conn = get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE members SET plan='None' WHERE name=%s", (member_name,))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    messagebox.showinfo("Deleted", f"Subscription removed for {member_name}!")
                    self.refresh_all()
                except Exception as e:
                    messagebox.showerror("Database Error", str(e))

    def on_subscription_select(self, event):
        """Table se row click karne par form me values auto-fill honge"""
        selected = self.table.selection()
        if selected:
            row = self.table.item(selected[0])['values']
            self.selected_member_name = row[1]
            
            # Auto fill member dropdown
            if row[1] in self.combo_member['values']:
                self.combo_member.set(row[1])

            # Auto fill start date
            self.txt_start_date.delete(0, tk.END)
            self.txt_start_date.insert(0, str(row[3]))

    def clear_form(self):
        """Form inputs aur selections clear karne ke liye"""
        self.selected_member_name = None
        self.txt_start_date.delete(0, tk.END)
        self.txt_start_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        if self.combo_member['values']:
            self.combo_member.current(0)
        self.combo_plan.current(0)
        if self.table.selection():
            self.table.selection_remove(self.table.selection())

    def refresh_all(self):
        """Dropdowns, table aur clear form ek sath refresh karega"""
        self.clear_form()
        self.load_members_dropdown()
        self.load_subscriptions()