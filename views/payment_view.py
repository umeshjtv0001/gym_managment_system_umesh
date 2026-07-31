import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from dao.payment_dao import PaymentDAO
from dao.member_dao import MemberDAO

class PaymentView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.payment_dao = PaymentDAO()
        self.member_dao = MemberDAO()

        # Title
        title_label = tk.Label(
            self, text="Payment History & Invoices", font=("Arial", 16, "bold"), bg="white", fg="#1e3a8a"
        )
        title_label.pack(anchor="w", padx=20, pady=(15, 5))

        # Record Payment Form
        form_frame = tk.LabelFrame(self, text="Record New Payment", font=("Arial", 10, "bold"), bg="white", padx=15, pady=10)
        form_frame.pack(fill="x", padx=20, pady=5)

        # Select Member Dropdown
        tk.Label(form_frame, text="Select Member:", bg="white").grid(row=0, column=0, sticky="w", pady=5)
        self.combo_members = ttk.Combobox(form_frame, state="readonly", width=25)
        self.combo_members.grid(row=0, column=1, padx=10, pady=5)

        # Amount
        tk.Label(form_frame, text="Amount (₹):", bg="white").grid(row=0, column=2, sticky="w", pady=5)
        self.txt_amount = tk.Entry(form_frame)
        self.txt_amount.insert(0, "1000")
        self.txt_amount.grid(row=0, column=3, padx=10, pady=5)

        # Payment Mode
        tk.Label(form_frame, text="Payment Mode:", bg="white").grid(row=1, column=0, sticky="w", pady=5)
        self.combo_mode = ttk.Combobox(form_frame, values=["Cash", "UPI / GPay", "Card", "Bank Transfer"], state="readonly")
        self.combo_mode.current(1)
        self.combo_mode.grid(row=1, column=1, padx=10, pady=5)

        # Payment Date
        tk.Label(form_frame, text="Date:", bg="white").grid(row=1, column=2, sticky="w", pady=5)
        self.txt_date = tk.Entry(form_frame)
        self.txt_date.insert(0, str(date.today()))
        self.txt_date.grid(row=1, column=3, padx=10, pady=5)

        # Payment Status
        tk.Label(form_frame, text="Status:", bg="white").grid(row=2, column=0, sticky="w", pady=5)
        self.combo_status = ttk.Combobox(form_frame, values=["Paid", "Unpaid", "Pending"], state="readonly")
        self.combo_status.current(0)
        self.combo_status.grid(row=2, column=1, padx=10, pady=5)

        # Buttons
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.grid(row=2, column=2, columnspan=2, pady=5, sticky="e")

        btn_save = tk.Button(
            btn_frame, text="Save Payment", bg="#22c55e", fg="white", 
            font=("Arial", 10, "bold"), bd=0, padx=15, pady=5, command=self.save_payment_action
        )
        btn_save.pack(side="left", padx=5)

        btn_refresh = tk.Button(
            btn_frame, text="Refresh History", bg="#3b82f6", fg="white", 
            font=("Arial", 10, "bold"), bd=0, padx=15, pady=5, command=self.load_payment_data
        )
        btn_refresh.pack(side="left", padx=5)

        # History Table Section
        table_frame = tk.Frame(self, bg="white")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("pay_id", "member", "amount", "mode", "date", "status")
        self.table = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.table.heading("pay_id", text="Payment ID")
        self.table.heading("member", text="Member Name")
        self.table.heading("amount", text="Amount (₹)")
        self.table.heading("mode", text="Payment Mode")
        self.table.heading("date", text="Payment Date")
        self.table.heading("status", text="Status")

        self.table.column("pay_id", width=80)
        self.table.column("member", width=150)
        self.table.column("amount", width=100)
        self.table.column("mode", width=110)
        self.table.column("date", width=110)
        self.table.column("status", width=90)

        self.table.pack(fill="both", expand=True)

        # Load initial dropdowns & table data
        self.member_map = {}
        self.load_members_dropdown()
        self.load_payment_data()

    def load_members_dropdown(self):
        members = self.member_dao.get_all_members()
        member_list = []
        self.member_map = {}
        
        for m in members:
            m_id = m.get("id") or m.get("member_id")
            m_name = m.get("name")
            display_str = f"{m_id} - {m_name}"
            member_list.append(display_str)
            self.member_map[display_str] = m_id

        self.combo_members['values'] = member_list
        if member_list:
            self.combo_members.current(0)

    def save_payment_action(self):
        selected_m = self.combo_members.get()
        if not selected_m:
            messagebox.showwarning("Validation", "Please select a member!")
            return

        member_id = self.member_map.get(selected_m)
        amount = self.txt_amount.get().strip()
        mode = self.combo_mode.get()
        pay_date = self.txt_date.get().strip()
        status = self.combo_status.get()

        if not amount:
            messagebox.showwarning("Validation", "Please enter amount!")
            return

        success, msg = self.payment_dao.add_payment(member_id, amount, mode, pay_date, status)
        if success:
            messagebox.showinfo("Success", msg)
            self.load_payment_data()
        else:
            messagebox.showerror("Error", msg)

    def load_payment_data(self):
        for row in self.table.get_children():
            self.table.delete(row)

        self.load_members_dropdown()
        payments = self.payment_dao.get_all_payments()
        
        for idx, p in enumerate(payments, start=1001):
            pay_id = f"PAY-{idx}"
            m_name = p.get("member_name") or "Unknown"
            amt = f"₹ {p.get('amount')}"
            mode = p.get("mode") or "Cash/UPI"
            pay_date = str(p.get("payment_date"))
            status = p.get("status") or "Paid"

            self.table.insert("", "end", values=(pay_id, m_name, amt, mode, pay_date, status))