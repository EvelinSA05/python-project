import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
import os
from datetime import datetime

DATA_FILE = "todo.json"

def load_tasks():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            if data and isinstance(data[0], str):
                return [{"task": t, "deadline": "Tidak ada"} for t in data]
            return data
    return []

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

class TodoApp:
    def check_deadline_alert(self):
        now = datetime.now()
        soon = []

        for t in self.tasks:
            try:
                deadline_time = datetime.strptime(t['deadline'], "%Y-%m-%d %H:%M")
                if 0 <= (deadline_time - now).total_seconds() <= 3600:
                    soon.append(f"🕒 {t['task']} (⏳ {t['deadline']})")
            except:
                continue

        if soon:
            messagebox.showinfo("🔔 Peringatan Deadline!", "Tugas berikut akan jatuh tempo dalam 1 jam:\n\n" + "\n".join(soon))

    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("650x450")

        self.tasks = load_tasks()
        self.task_var = tk.StringVar()
        self.deadline_var = tk.StringVar()

        self.dark_mode = False

        self.create_widgets()
        self.refresh_table()

        self.check_deadline_alert()  # Panggil alert setelah load data

    def create_widgets(self):
        self.root.configure(bg="#f0f4f8")

        title = tk.Label(self.root, text="📝 To-Do List with Deadline", font=("Segoe UI", 16, "bold"), bg="#f0f4f8")
        title.pack(pady=10)

        form_frame = tk.Frame(self.root, bg="#f0f4f8")
        form_frame.pack(pady=5)

        tk.Label(form_frame, text="Tugas:", bg="#f0f4f8", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w")
        tk.Entry(form_frame, textvariable=self.task_var, width=45, font=("Segoe UI", 10)).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Deadline (YYYY-MM-DD HH:MM):", bg="#f0f4f8", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w")
        tk.Entry(form_frame, textvariable=self.deadline_var, width=30, font=("Segoe UI", 10)).grid(row=1, column=1, padx=5, pady=5)

        button_frame = tk.Frame(self.root, bg="#f0f4f8")
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="➕ Tambah", width=15, command=self.add_task, bg="#4caf50", fg="white", font=("Segoe UI", 10)).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="🗑 Hapus", width=15, command=self.delete_task, bg="#f44336", fg="white", font=("Segoe UI", 10)).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="🔔 Cek Pengingat", width=15, command=self.check_deadline_alert, bg="#ff9800", fg="white", font=("Segoe UI", 10)).grid(row=0, column=2, padx=5)

        # Treeview for task list
        self.tree = ttk.Treeview(self.root, columns=("Task", "Deadline"), show="headings", height=12)
        self.tree.heading("Task", text="Tugas", anchor=tk.W)
        self.tree.heading("Deadline", text="Deadline", anchor=tk.W)
        self.tree.column("Task", width=300, anchor=tk.W)
        self.tree.column("Deadline", width=180, anchor=tk.W)
        self.tree.pack(pady=10)

    def add_task(self):
        task = self.task_var.get().strip()
        deadline = self.deadline_var.get().strip()

        if not task or not deadline:
            messagebox.showwarning("Peringatan", "Tugas dan deadline tidak boleh kosong.")
            return

        try:
            datetime.strptime(deadline, "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Error", "Format deadline salah.\nContoh: 2025-04-25 14:30")
            return

        self.tasks.append({"task": task, "deadline": deadline})
        self.task_var.set("")
        self.deadline_var.set("")
        save_tasks(self.tasks)
        self.refresh_table()

    def delete_task(self):
        selected_item = self.tree.selection()
        if selected_item:
            task_to_delete = self.tree.item(selected_item[0])["values"]
            self.tasks = [t for t in self.tasks if t["task"] != task_to_delete[0]]
            save_tasks(self.tasks)
            self.refresh_table()
        else:
            messagebox.showwarning("Peringatan", "Pilih tugas yang ingin dihapus.")

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        bg = "#1e1e1e" if self.dark_mode else "#f0f4f8"
        fg = "#ffffff" if self.dark_mode else "#000000"
        listbox_bg = "#2d2d2d" if self.dark_mode else "white"

        self.root.configure(bg=bg)
        for widget in self.root.winfo_children():
            if isinstance(widget, (tk.Label, tk.Frame)):
                widget.configure(bg=bg)
            if isinstance(widget, tk.Button):
                widget.configure(bg="#607d8b" if not self.dark_mode else "#3a3a3a", fg=fg)
        self.tree.configure(style="Treeview", background=listbox_bg, foreground=fg)

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            sorted_tasks = sorted(self.tasks, key=lambda x: datetime.strptime(x['deadline'], "%Y-%m-%d %H:%M"))
        except:
            sorted_tasks = self.tasks

        for t in sorted_tasks:
            self.tree.insert("", "end", values=(t["task"], t["deadline"]))

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
