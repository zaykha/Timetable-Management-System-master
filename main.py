import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os, sys
sys.path.insert(0, 'windows/')



def open_student_window():
    m.destroy()
    os.system('py windows\\schedule.py')
    # sys.exit()


   

m = tk.Tk()

m.geometry('400x430')
m.title('Welcome')

tk.Label(
    m,
    text='PSB ACADEMY TIMETABLING AND SCHEDULER VIEWER',
    font=('Consolas', 20, 'bold'),
    wrap=400
).pack(pady=20)

tk.Label(
    m,
    text='Welcome!\nto Timetable Viewer and Generator App',
    font=('Consolas', 12, 'italic')
).pack(pady=10)


tk.Button(
    m,
    text='Start',
    font=('Consolas', 12, 'bold'),
    padx=30,
    command=open_student_window
).pack(pady=10)

m.mainloop()