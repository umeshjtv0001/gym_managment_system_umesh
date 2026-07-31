import tkinter as tk
from tkinter import ttk, messagebox
from database.connection import get_db_connection

class UserView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")

        # Title Header
        title_label = tk.Label(
            self, text="System Staff, Admins & Owners Management", font=("Arial", 16, "bold"), bg="white", fg="#1e3a8a"
        )
        title_label.pack(anchor="w", padx=20, pady=(15, 5))

        # ------------------- Form Controls Frame -------------------
        form_frame = tk.LabelFrame(self, text="Add / Edit System User", font=("Arial", 10, "bold"), bg="white", padx=15, pady=10)
        form_frame.pack(fill="x", padx=20, pady=5)

        # Row 0: Username & Password
        tk.Label(form_frame, text="Username:", bg="white", font=("Arial", 9)).grid(row=0, column=0, sticky="w", pady=5)
        self.txt_username = tk.Entry(form_frame, width=22)
        self.txt_username.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Password:", bg="white", font=("Arial", 9)).grid(row=0, column=2, sticky="w", pady=5)
        self.txt_password = tk.Entry(form_frame, width=22, show="*")
        self.txt_password.grid(row=0, column=3, padx=10, pady=5)

        # Row 1: Role Dropdown
        tk.Label(form_frame, text="Role:", bg="white", font=("Arial", 9)).grid(row=1, column=0, sticky="w", pady=5)
        self.cmb_role = ttk.Combobox(form_frame, values=["Owner", "Administrator", "Staff / Trainer"], width=20, state="readonly")
        self.cmb_role.grid(row=1, column=1, padx=10, pady=5)
        self.cmb_role.set("Owner")

        # Buttons
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.grid(row=2, column=0, columnspan=4, pady=(10, 5), sticky="w")

        tk.Button(
            btn_frame, text="Add User", bg="#22c55e", fg="white", 
            font=("Arial", 9, "bold"), bd=0, padx=12, pady=5, command=self.add_user
        ).pack(side="left", padx=4)

        tk.Button(
            btn_frame, text="Delete User", bg="#ef4444", fg="white", 
            font=("Arial", 9, "bold"), bd=0, padx=12, pady=5, command=self.delete_user
        ).pack(side="left", padx=4)

        tk.Button(
            btn_frame, text="Clear Form", bg="#6b7280", fg="white", 
            font=("Arial", 9, "bold"), bd=0, padx=12, pady=5, command=self.clear_form
        ).pack(side="left", padx=4)

        # ------------------- Search & Refresh Bar -------------------
        filter_frame = tk.Frame(self, bg="white")
        filter_frame.pack(fill="x", padx=20, pady=(10, 5))

        tk.Label(filter_frame, text="Search User:", font=("Arial", 9, "bold"), bg="white").pack(side="left", padx=(0, 5))
        self.txt_search = tk.Entry(filter_frame, width=25)
        self.txt_search.pack(side="left", padx=5)
        self.txt_search.bind("<KeyRelease>", self.filter_users)

        tk.Button(
            filter_frame, text="🔄 Refresh Data", bg="#0284c7", fg="white", 
            font=("Arial", 9, "bold"), bd=0, padx=12, pady=3, command=self.refresh_all
        ).pack(side="right", padx=5)

        # ------------------- Table Frame -------------------
        table_frame = tk.Frame(self, bg="white")
        table_frame.pack(fill="both", expand=True, padx=20, pady=(5, 15))

        columns = ("user_id", "username", "role")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.table.heading("user_id", text="User ID")
        self.table.heading("username", text="Username")
        self.table.heading("role", text="Role")

        self.table.column("user_id", width=100, anchor="center")
        self.table.column("username", width=250)
        self.table.column("role", width=250)

        self.table.pack(fill="both", expand=True)

        self.table.bind("<<TreeviewSelect>>", self.on_user_select)

        self.all_users = []
        self.selected_user_id = None

        self.setup_db_table()
        self.refresh_all()

    def setup_db_table(self):
        """Database Table Fix Logic: Ensures 'role' column exists in 'users' table"""
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                
                # 1. Create table if not exists
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(50) NOT NULL UNIQUE,
                        password VARCHAR(255) NOT NULL,
                        role VARCHAR(50) DEFAULT 'Staff / Trainer'
                    )
                """)

                # 2. Add 'role' column automatically if table exists but column is missing
                try:
                    cursor.execute("ALTER TABLE users ADD COLUMN role VARCHAR(50) DEFAULT 'Staff / Trainer'")
                except Exception:
                    pass  # Column already exists

                conn.commit()
                cursor.close()
                conn.close()
            except Exception as e:
                print("Error setting up users table:", e)

    def load_users(self):
        for row in self.table.get_children():
            self.table.delete(row)

        conn = get_db_connection()
        self.all_users = []
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("SELECT * FROM users ORDER BY id ASC")
                rows = cursor.fetchall()

                for r in rows:
                    role_val = r.get('role', 'Staff / Trainer') or 'Staff / Trainer'
                    user_data = (r['id'], r['username'], role_val)
                    self.all_users.append(user_data)
                    self.table.insert("", "end", values=user_data)

                cursor.close()
                conn.close()
            except Exception as e:
                print("Error loading users:", e)

    def filter_users(self, event=None):
        query = self.txt_search.get().strip().lower()
        for row in self.table.get_children():
            self.table.delete(row)

        for u in self.all_users:
            if query in str(u[1]).lower() or query in str(u[2]).lower():
                self.table.insert("", "end", values=u)

    def add_user(self):
        username = self.txt_username.get().strip()
        password = self.txt_password.get().strip()
        role = self.cmb_role.get().strip()

        if not username or not password or not role:
            messagebox.showwarning("Warning", "Please fill all fields!")
            return

        conn = get_db_connection()
        if not conn:
            messagebox.showerror("Error", "Database connection failed!")
            return

        try:
            cursor = conn.cursor()
            
            # Duplicate Username check
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                messagebox.showwarning("Duplicate", f"Username '{username}' already exists! Choose another name.")
                cursor.close()
                conn.close()
                return

            cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Success", f"User '{username}' with role '{role}' added successfully!")
            self.refresh_all()

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to add user:\n{e}")

    def delete_user(self):
        if not self.selected_user_id:
            messagebox.showwarning("Selection Required", "Please select a user to delete!")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this user?"):
            conn = get_db_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM users WHERE id=%s", (self.selected_user_id,))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    messagebox.showinfo("Deleted", "User deleted successfully!")
                    self.refresh_all()
                except Exception as e:
                    messagebox.showerror("Database Error", str(e))

    def on_user_select(self, event):
        selected = self.table.selection()
        if selected:
            row = self.table.item(selected[0])['values']
            self.selected_user_id = row[0]

            self.txt_username.delete(0, tk.END)
            self.txt_username.insert(0, str(row[1]))

            self.cmb_role.set(str(row[2]))

    def clear_form(self):
        self.selected_user_id = None
        self.txt_username.delete(0, tk.END)
        self.txt_password.delete(0, tk.END)
        self.txt_search.delete(0, tk.END)
        self.cmb_role.set("Owner")
        if self.table.selection():
            self.table.selection_remove(self.table.selection())

    def refresh_all(self):
        self.clear_form()
        self.load_users()