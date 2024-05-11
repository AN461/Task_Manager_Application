import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime

class TaskManagerApp:
    def __init__(self, master):
        self.master = master
        master.title("Task Manager")

        # Set window size
        master.geometry("900x800")  # Width x Height

        self.tasks = []

        self.task_title_label = ttk.Label(master, text="Task Title:")
        self.task_title_label.grid(row=0, column=0, padx=5, pady=5)
        self.task_title_entry = ttk.Entry(master)
        self.task_title_entry.grid(row=0, column=1, padx=5, pady=5)

        self.task_description_label = ttk.Label(master, text="Task Description:")
        self.task_description_label.grid(row=1, column=0, padx=5, pady=5)
        self.task_description_entry = ttk.Entry(master)
        self.task_description_entry.grid(row=1, column=1, padx=5, pady=5)

        self.due_date_label = ttk.Label(master, text="Due Date:")
        self.due_date_label.grid(row=2, column=0, padx=5, pady=5)
        self.due_date_entry = DateEntry(master, date_pattern="dd/mm/yyyy")
        self.due_date_entry.grid(row=2, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(master, text="Add Task", command=self.add_task)
        self.add_button.grid(row=3, column=1, padx=5, pady=5)

        self.canvas = tk.Canvas(master)
        self.scrollbar = ttk.Scrollbar(master, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.task_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.task_frame, anchor="nw")

        self.scrollbar.grid(row=4, column=2, sticky="nswe")
        self.canvas.grid(row=4, column=0, columnspan=3, sticky="nsew")

        self.task_frame.bind("<Configure>", self.on_frame_configure)
        master.grid_rowconfigure(4, weight=1)
        master.grid_columnconfigure(1, weight=1)

    def add_task(self):
        title = self.task_title_entry.get()
        description = self.task_description_entry.get()
        due_date = self.due_date_entry.get()

        if title and description and due_date:
            task_info = f"Title: {title}\nDescription: {description}\nDue Date: {due_date}"
            task_box = ttk.LabelFrame(self.task_frame, text=f"Task-{len(self.tasks) + 1}")
            task_label = ttk.Label(task_box, text=task_info)
            task_label.pack(padx=5, pady=5, anchor=tk.W)
            remove_button = ttk.Button(task_box, text="Remove Task", command=lambda: self.remove_task(task_box))
            remove_button.pack(side=tk.RIGHT, padx=5, pady=5)
            task_box.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
            self.tasks.append((title, description, due_date))
            self.update_task_timer(task_box, due_date)
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def remove_task(self, task_box):
        task_box.destroy()
        self.tasks.pop()

    def update_task_timer(self, task_box, due_date):
        def update():
            now = datetime.now()
            due_datetime = datetime.strptime(due_date, "%d/%m/%Y")
            remaining_time = due_datetime - now
            remaining_time_str = f"Time Left: {remaining_time.days} days, {remaining_time.seconds // 3600} hours, {(remaining_time.seconds // 60) % 60} minutes, {remaining_time.seconds % 60} seconds"
            remaining_time_label.config(text=remaining_time_str)
            self.master.after(1000, update)  # Update every second

        remaining_time_label = ttk.Label(task_box)
        remaining_time_label.pack(side=tk.TOP, anchor=tk.E)
        update()  # Start the timer

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

def main():
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
