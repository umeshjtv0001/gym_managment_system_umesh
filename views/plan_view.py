import tkinter as tk
from tkinter import ttk, messagebox
from database.connection import get_db_connection

class PlanView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")

        # Title
        title_label = tk.Label(
            self, text="Gym Membership Plans", font=("Arial", 16, "bold"), bg="white", fg="#1e3a8a"
        )
        title_label.pack(anchor="w", padx=20, pady=(15, 5))

        # ------------------- Form Controls Frame -------------------
        form_frame = tk.LabelFrame(self, text="Add / Edit Plan", font=("Arial", 10, "bold"), bg="white", padx=15, pady=10)
        form_frame.pack(fill="x", padx=20, pady=5)

        # Row 0: Plan Name & Duration
        tk.Label(form_frame, text="Plan Name:", bg="white", font=("Arial", 9)).grid(row=0, column=0, sticky="w", pady=5)
        self.txt_plan_name = tk.Entry(form_frame, width=22)
        self.txt_plan_name.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Duration (Months):", bg="white", font=("Arial", 9)).grid(row=0, column=2, sticky="w", pady=5)
        self.txt_duration = tk.Entry(form_frame, width=22)
        self.txt_duration.grid(row=0, column=3, padx=10, pady=5)

        # Row 1: Price
        tk.Label(form_frame, text="Price (₹):", bg="white", font=("Arial", 9)).grid(row=1, column=0, sticky="w", pady=5)
        self.txt_price = tk.Entry(form_frame, width=22)
        self.txt_price.grid(row=1, column=1, padx=10, pady=5)

        # Buttons
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.grid(row=2, column=0, columnspan=4, pady=(10, 5), sticky="w")

        tk.Button(
            btn_frame, text="Add Plan", bg="#22c55e", fg="white", 
            font=("Arial", 9, "bold"), bd=0, padx=12, pady=5, command=self.add_plan
        ).pack(side="left", padx=4)

        tk.Button(
            btn_frame, text="Update Plan", bg="#3b82f6", fg="white", 
            font=("Arial", 9, "bold"), bd=0, padx=12, pady=5, command=self.update_plan
        ).pack(side="left", padx=4)

        tk.Button(
            btn_frame, text="Delete Plan", bg="#ef4444", fg="white", 
            font=("Arial", 9, "bold"), bd=0, padx=12, pady=5, command=self.delete_plan
        ).pack(side="left", padx=4)

        tk.Button(
            btn_frame, text="Clear Form", bg="#6b7280", fg="white", 
            font=("Arial", 9, "bold"), bd=0, padx=12, pady=5, command=self.clear_form
        ).pack(side="left", padx=4)

        # ------------------- Search & Refresh Bar -------------------
        filter_frame = tk.Frame(self, bg="white")
        filter_frame.pack(fill="x", padx=20, pady=(10, 5))

        tk.Label(filter_frame, text="Search Plan:", font=("Arial", 9, "bold"), bg="white").pack(side="left", padx=(0, 5))
        self.txt_search = tk.Entry(filter_frame, width=25)
        self.txt_search.pack(side="left", padx=5)
        self.txt_search.bind("<KeyRelease>", self.filter_plans)

        tk.Button(
            filter_frame, text="🔄 Refresh Data", bg="#0284c7", fg="white", 
            font=("Arial", 9, "bold"), bd=0, padx=12, pady=3, command=self.refresh_all
        ).pack(side="right", padx=5)

        # ------------------- Table Frame -------------------
        table_frame = tk.Frame(self, bg="white")
        table_frame.pack(fill="both", expand=True, padx=20, pady=(5, 15))

        columns = ("plan_id", "plan_name", "duration", "price")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.table.heading("plan_id", text="Plan ID")
        self.table.heading("plan_name", text="Plan Name")
        self.table.heading("duration", text="Duration")
        self.table.heading("price", text="Price")

        self.table.column("plan_id", width=100, anchor="center")
        self.table.column("plan_name", width=250)
        self.table.column("duration", width=150, anchor="center")
        self.table.column("price", width=150, anchor="center")

        self.table.pack(fill="both", expand=True)
        self.table.bind("<<TreeviewSelect>>", self.on_plan_select)

        self.all_plans = []
        self.selected_plan_id = None

        self.setup_db_table()
        self.refresh_all()

    def setup_db_table(self):
        """Auto Table Setup and Column Check"""
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS plans (
                        plan_id INT AUTO_INCREMENT PRIMARY KEY,
                        plan_name VARCHAR(100) NOT NULL,
                        duration INT NOT NULL,
                        price DECIMAL(10, 2) NOT NULL
                    )
                """)
                conn.commit()
                cursor.close()
                conn.close()
            except Exception as e:
                print("Error setting up plans table:", e)

    def load_plans(self):
        """Fetches data using dynamic column identification to prevent SQL errors"""
        for row in self.table.get_children():
            self.table.delete(row)

        conn = get_db_connection()
        self.all_plans = []
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                # Select all without strict ordering column assumptions
                cursor.execute("SELECT * FROM plans")
                rows = cursor.fetchall()

                for r in rows:
                    # Check for column key flexibly (id vs plan_id, name vs plan_name)
                    p_id = r.get('plan_id') or r.get('id')
                    p_name = r.get('plan_name') or r.get('name') or r.get('title')
                    p_dur = r.get('duration') or r.get('duration_months') or 0
                    p_price = r.get('price') or r.get('cost') or 0.0

                    plan_tuple = (p_id, p_name, f"{p_dur} Months" if str(p_dur).isdigit() else p_dur, f"₹{p_price}")
                    self.all_plans.append(plan_tuple)
                    self.table.insert("", "end", values=plan_tuple)

                cursor.close()
                conn.close()
            except Exception as e:
                print(f"Error loading plans: {e}")

    def filter_plans(self, event=None):
        query = self.txt_search.get().strip().lower()
        for row in self.table.get_children():
            self.table.delete(row)

        for p in self.all_plans:
            if query in str(p[1]).lower():
                self.table.insert("", "end", values=p)

    def add_plan(self):
        name = self.txt_plan_name.get().strip()
        duration = self.txt_duration.get().strip()
        price = self.txt_price.get().strip()

        if not name or not duration or not price:
            messagebox.showwarning("Warning", "Please fill all fields!")
            return

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                # Determine correct column names
                cursor.execute("SHOW COLUMNS FROM plans")
                cols = [c[0] for c in cursor.fetchall()]

                id_col = 'plan_id' if 'plan_id' in cols else 'id'
                name_col = 'plan_name' if 'plan_name' in cols else 'name'

                query = f"INSERT INTO plans ({name_col}, duration, price) VALUES (%s, %s, %s)"
                cursor.execute(query, (name, duration, price))
                conn.commit()
                cursor.close()
                conn.close()

                messagebox.showinfo("Success", f"Plan '{name}' added successfully!")
                self.refresh_all()
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to add plan:\n{e}")

    def update_plan(self):
        if not self.selected_plan_id:
            messagebox.showwarning("Selection Required", "Please select a plan from table to update!")
            return

        name = self.txt_plan_name.get().strip()
        duration = self.txt_duration.get().strip().replace(" Months", "")
        price = self.txt_price.get().strip().replace("₹", "")

        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SHOW COLUMNS FROM plans")
                cols = [c[0] for c in cursor.fetchall()]

                id_col = 'plan_id' if 'plan_id' in cols else 'id'
                name_col = 'plan_name' if 'plan_name' in cols else 'name'

                query = f"UPDATE plans SET {name_col}=%s, duration=%s, price=%s WHERE {id_col}=%s"
                cursor.execute(query, (name, duration, price, self.selected_plan_id))
                conn.commit()
                cursor.close()
                conn.close()

                messagebox.showinfo("Updated", "Plan updated successfully!")
                self.refresh_all()
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to update plan:\n{e}")

    def delete_plan(self):
        if not self.selected_plan_id:
            messagebox.showwarning("Selection Required", "Please select a plan to delete!")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this plan?"):
            conn = get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("SHOW COLUMNS FROM plans")
                    cols = [c[0] for c in cursor.fetchall()]
                    id_col = 'plan_id' if 'plan_id' in cols else 'id'

                    cursor.execute(f"DELETE FROM plans WHERE {id_col}=%s", (self.selected_plan_id,))
                    conn.commit()
                    cursor.close()
                    conn.close()

                    messagebox.showinfo("Deleted", "Plan deleted successfully!")
                    self.refresh_all()
                except Exception as e:
                    messagebox.showerror("Database Error", str(e))

    def on_plan_select(self, event):
        selected = self.table.selection()
        if selected:
            row = self.table.item(selected[0])['values']
            self.selected_plan_id = row[0]

            self.txt_plan_name.delete(0, tk.END)
            self.txt_plan_name.insert(0, str(row[1]))

            self.txt_duration.delete(0, tk.END)
            self.txt_duration.insert(0, str(row[2]).replace(" Months", ""))

            self.txt_price.delete(0, tk.END)
            self.txt_price.insert(0, str(row[3]).replace("₹", ""))

    def clear_form(self):
        self.selected_plan_id = None
        self.txt_plan_name.delete(0, tk.END)
        self.txt_duration.delete(0, tk.END)
        self.txt_price.delete(0, tk.END)
        self.txt_search.delete(0, tk.END)
        if self.table.selection():
            self.table.selection_remove(self.table.selection())

    def refresh_all(self):
        self.clear_form()
        self.load_plans()