import sys
import os
import traceback
import tkinter as tk
from tkinter import messagebox

# Root path add kar rahe hain
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from views.dashboard import Dashboard

def main():
    try:
        app = Dashboard()
        app.mainloop()
    except Exception as e:
        error_msg = traceback.format_exc()
        print("Application Error Log:")
        print(error_msg)
        
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Application Error", f"An unexpected error occurred:\n\n{e}")

if __name__ == "__main__":
    main()