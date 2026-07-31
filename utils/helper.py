from tkinter import messagebox

class Helper:

    @staticmethod
    def success(msg):
        messagebox.showinfo("Success", msg)

    @staticmethod
    def error(msg):
        messagebox.showerror("Error", msg)

    @staticmethod
    def warning(msg):
        messagebox.showwarning("Warning", msg)