import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from dao.member_dao import MemberDAO

class MemberView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.member_dao = MemberDAO()
        self.selected_member_id = None

        # Title
        title_label = tk.Label(
            self, text="Member Management", font=("Arial", 16, "bold"), bg="white", fg="#1e3a8a"
        )
        title_label.pack(anchor="w", padx=20, pady=(15, 5))

        # Form Section
        form_frame = tk.LabelFrame(self, text="Member Details", font=("Arial", 10, "bold"), bg="white", padx=15, pady=10)
        form_frame.pack(fill="x", padx=20, pady=5)

        # Name
        tk.Label(form_frame, text="Name:", bg="white").grid(row=0, column=0, sticky="w", pady=5)
        self.txt_name = tk.Entry(form_frame)
        self.txt_name.grid(row=0, column=1, padx=10, pady=5)

        # Phone
        tk.Label(form_frame, text="Phone:", bg="white").grid(row=0, column=2, sticky="w", pady=5)
        self.txt_phone = tk.Entry(form_frame)
        self.txt_phone.grid(row=0, column=3, padx=10, pady=5)

        # Gender
        tk.Label(form_frame, text="Gender:", bg="white").grid(row=1, column=0, sticky="w", pady=5)
        self.combo_gender = ttk.Combobox(form_frame, values=["Male", "Female", "Other"], state="readonly")
        self.combo_gender.current(0)
        self.combo_gender.grid(row=1, column=1, padx=10, pady=5)

        # Plan
        tk.Label(form_frame, text="Plan:", bg="white").grid(row=1, column=2, sticky="w", pady=5)
        self.combo_plan = ttk.Combobox(form_frame, values=["Monthly Basic", "Quarterly Pro", "Yearly VIP"], state="readonly")
        self.combo_plan.current(0)
        self.combo_plan.grid(row=1, column=3, padx=10, pady=5)

        # Payment Status
        tk.Label(form_frame, text="Payment Status:", bg="white").grid(row=2, column=0, sticky="w", pady=5)
        self.combo_status = ttk.Combobox(form_frame, values=["Paid", "Unpaid", "Pending"], state="readonly")
        self.combo_status.current(0)
        self.combo_status.grid(row=2, column=1, padx=10, pady=5)

        # Buttons Frame
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.grid(row=3, column=0, columnspan=4, pady=10, sticky="w")

        self.btn_add = tk.Button(
            btn_frame, text="Add Member", bg="#22c55e", fg="white", 
            font=("Arial", 10, "bold"), bd=0, padx=15, pady=5, command=self.add_member_action
        )
        self.btn_add.pack(side="left", padx=5)

        self.btn_update = tk.Button(
            btn_frame, text="Update Member", bg="#3b82f6", fg="white", 
            font=("Arial", 10, "bold"), bd=0, padx=15, pady=5, command=self.update_member_action
        )
        self.btn_update.pack(side="left", padx=5)

        self.btn_delete = tk.Button(
            btn_frame, text="Delete Member", bg="#ef4444", fg="white", 
            font=("Arial", 10, "bold"), bd=0, padx=15, pady=5, command=self.delete_member_action
        )
        self.btn_delete.pack(side="left", padx=5)

        self.btn_clear = tk.Button(
            btn_frame, text="Clear", bg="#6b7280", fg="white", 
            font=("Arial", 10, "bold"), bd=0, padx=15, pady=5, command=self.clear_form
        )
        self.btn_clear.pack(side="left", padx=5)

        # Data Table
        table_frame = tk.Frame(self, bg="white")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("id", "name", "phone", "gender", "plan", "status")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.table.heading("id", text="ID")
        self.table.heading("name", text="Name")
        self.table.heading("phone", text="Phone")
        self.table.heading("gender", text="Gender")
        self.table.heading("plan", text="Plan")
        self.table.heading("status", text="Payment Status")

        self.table.column("id", width=40)
        self.table.column("name", width=140)
        self.table.column("phone", width=110)
        self.table.column("gender", width=70)
        self.table.column("plan", width=110)
        self.table.column("status", width=110)

        self.table.pack(fill="both", expand=True)

        self.table.bind("<<TreeviewSelect>>", self.on_member_select)

        self.load_members()

    def add_member_action(self):
        name = self.txt_name.get().strip()
        phone = self.txt_phone.get().strip()
        gender = self.combo_gender.get()
        plan = self.combo_plan.get()
        status = self.combo_status.get()

        if not name or not phone:
            messagebox.showwarning("Validation", "Please fill Name and Phone fields!")
            return

        success, msg = self.member_dao.add_member(name, phone, gender, plan, status)

        if success:
            messagebox.showinfo("Success", msg)
            self.clear_form()
            self.load_members()
        else:
            messagebox.showerror("Error", msg)

    def update_member_action(self):
        if not self.selected_member_id:
            messagebox.showwarning("Selection Error", "Please select a member from table to edit!")
            return

        name = self.txt_name.get().strip()
        phone = self.txt_phone.get().strip()
        gender = self.combo_gender.get()
        plan = self.combo_plan.get()
        status = self.combo_status.get()

        if not name or not phone:
            messagebox.showwarning("Validation", "Please fill Name and Phone fields!")
            return

        success, msg = self.member_dao.update_member(self.selected_member_id, name, phone, gender, plan, status)

        if success:
            messagebox.showinfo("Success", msg)
            self.clear_form()
            self.load_members()
        else:
            messagebox.showerror("Error", msg)

    def delete_member_action(self):
        if not self.selected_member_id:
            messagebox.showwarning("Selection Error", "Please select a member from table to delete!")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this member?"):
            success, msg = self.member_dao.delete_member(self.selected_member_id)
            if success:
                messagebox.showinfo("Success", msg)
                self.clear_form()
                self.load_members()
            else:
                messagebox.showerror("Error", msg)

    def on_member_select(self, event):
        selected = self.table.selection()
        if selected:
            row = self.table.item(selected[0])['values']
            self.selected_member_id = row[0]
            
            self.txt_name.delete(0, tk.END)
            self.txt_name.insert(0, str(row[1]))
            
            self.txt_phone.delete(0, tk.END)
            self.txt_phone.insert(0, str(row[2]))
            
            if row[3] in ["Male", "Female", "Other"]:
                self.combo_gender.set(row[3])
                
            if row[4] in ["Monthly Basic", "Quarterly Pro", "Yearly VIP"]:
                self.combo_plan.set(row[4])

            if len(row) > 5 and row[5] in ["Paid", "Unpaid", "Pending"]:
                self.combo_status.set(row[5])

    def clear_form(self):
        self.selected_member_id = None
        self.txt_name.delete(0, tk.END)
        self.txt_phone.delete(0, tk.END)
        self.combo_gender.current(0)
        self.combo_plan.current(0)
        self.combo_status.current(0)
        if self.table.selection():
            self.table.selection_remove(self.table.selection())

    def load_members(self):
        for row in self.table.get_children():
            self.table.delete(row)

        members = self.member_dao.get_all_members()
        for m in members:
            m_id = m.get("id") or m.get("member_id") or ""
            m_name = m.get("name") or ""
            m_phone = m.get("phone") or ""
            m_gender = m.get("gender") or ""
            m_plan = m.get("plan") or m.get("plan_id") or ""
            m_status = m.get("payment_status") or m.get("status") or "Paid"
            
            self.table.insert("", "end", values=(m_id, m_name, m_phone, m_gender, m_plan, m_status))