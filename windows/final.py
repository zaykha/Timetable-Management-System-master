import tkinter as tk
import pandas as pd
from tkinter import ttk

# Sample data (replace this with your actual data)
data = [
    {"Module": "Math", "Lecturer": "Mr. Smith", "Module Schedule": "Monday 10:00 AM", "Remarks": "Good"},
    {"Module": "Math", "Lecturer": "Mr. Smith", "Module Schedule": "Wednesday 2:00 PM", "Remarks": "Excellent"},
    {"Module": "Science", "Lecturer": "Ms. Johnson", "Module Schedule": "Tuesday 11:00 AM", "Remarks": "Average"},
    {"Module": "English", "Lecturer": "Mr. Davis", "Module Schedule": "Thursday 3:00 PM", "Remarks": "Good"},
    {"Module": "Science", "Lecturer": "Ms. Johnson", "Module Schedule": "Friday 1:00 PM", "Remarks": "Excellent"},
]


# Create the GUI
root = tk.Tk()
root.title("Schedule Data")

# Group data by Module and Lecturer
df = pd.DataFrame(data)
grouped = df.groupby(['Module', 'Lecturer']).agg(lambda x: ', '.join(x)).reset_index()

# Create a Treeview widget
treeview = ttk.Treeview(root, columns=("Module", "Lecturer", "Module Schedule", "Remarks"), show="headings")
treeview.heading("Module", text="Module")
treeview.heading("Lecturer", text="Lecturer")
treeview.heading("Module Schedule", text="Module Schedule")
treeview.heading("Remarks", text="Remarks")

# Insert data into the Treeview
for index, row in grouped.iterrows():
    treeview.insert("", "end", values=(row['Module'], row['Lecturer'], row['Module Schedule'], row['Remarks']))

treeview.pack()

root.mainloop()
