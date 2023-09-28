import tkinter as tk
import pandas as pd
from tkinter import ttk

# Define the number of days and periods
days = 5
week = 6

# Create labels for day names and period names
day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
period_names = list(map(lambda x: 'Week ' + str(x), range(1, week + 1)))

# Sample data (replace this with your actual data)
data = [
    {"Module": "Math", "Lecturer": "Mr. Smith", "Module Schedule": "Monday 10:00 AM", "Remarks": "Good"},
    {"Module": "Math", "Lecturer": "Mr. Smith", "Module Schedule": "Wednesday 2:00 PM", "Remarks": "Excellent"},
    {"Module": "Science", "Lecturer": "Ms. Johnson", "Module Schedule": "Tuesday 11:00 AM", "Remarks": "Average"},
    {"Module": "English", "Lecturer": "Mr. Davis", "Module Schedule": "Thursday 3:00 PM", "Remarks": "Good"},
    {"Module": "Science", "Lecturer": "Ms. Johnson", "Module Schedule": "Friday 1:00 PM", "Remarks": "Excellent"},
]

# Sample data for the Treeview (replace with your actual data)
sample_data = [
    ("Module A", "Week 1", "8:30-11:30|12:00-15:00|3:30-6:30"),
    ("", "Week 2", "9:00-1:00|1:00-4:00|4:00-7:00"),  # Empty module name
    (None, "Week 3", "10:00-2:00|2:00-5:00|5:00-8:00"),  # None module name
    ("Module B", "Week 4", "9:30-1:30|1:30-4:30|4:30-7:30"),
    # Add more data as needed
]

# Group data by Module and Lecturer
df = pd.DataFrame(data)
grouped = df.groupby(['Module', 'Lecturer']).agg(lambda x: ', '.join(x)).reset_index()

# Create the GUI
root = tk.Tk()
root.title("Schedule Data")

# Create a single frame to hold both the schedule grid and module information
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Create a Treeview widget for module information
module_treeview = ttk.Treeview(frame, columns=("Module", "Lecturer", "Module Schedule", "Remarks"), show="headings")
module_treeview.heading("Module", text="Module")
module_treeview.heading("Lecturer", text="Lecturer")
module_treeview.heading("Module Schedule", text="Module Schedule")
module_treeview.heading("Remarks", text="Remarks")

for index, row in grouped.iterrows():
    module_treeview.insert("", "end", values=(row['Module'], row['Lecturer'], row['Module Schedule'], row['Remarks']))

# Place the Treeview widget using the grid() method
module_treeview.grid(row=0, column=0, columnspan=len(day_names) + 1)

# Create a Treeview widget with sample data (you can replace this with your actual data)
schedule_treeview = ttk.Treeview(frame, columns=["Module", *day_names])
for data in sample_data:
    module_name, week_label, time_slots = data
    schedule_treeview.insert("", "end", values=[module_name, week_label] + [time_slots] * len(day_names))
# Calculate the width for the columns
column_width = 15  # Adjust this width as needed

# Create labels for day names (top row)
for i, day in enumerate(day_names):
    label = tk.Label(frame, text=day, width=column_width, height=2, bg='yellow', bd=1, relief='solid')
    label.grid(row=1, column=i + 1)

# Create labels for period names (left column)
for i, period in enumerate(period_names):
    label = tk.Label(frame, text=period, width=10, height=2, bg='yellow', bd=1, relief='solid')
    label.grid(row=i + 2, column=0)  # First column

# Create labels for module name, time slots, and schedule date from the Treeview data
for i, item in enumerate(schedule_treeview.get_children()):
    values = schedule_treeview.item(item, "values")
    module_name, week_label, time_slots = values[0], values[1], values[2:]

    for j in range(len(day_names)):
        module_text = module_name if module_name and module_name.strip() != "" else "-"
        cell_bg_color = 'white' if week_label == "Week 1" else 'yellow'

        # Set the same row height for all rows
        cell_height = 3

        time_and_date_label = tk.Label(frame, text=f"{time_slots[j]}\n{week_label}\n{module_text}", width=column_width, height=cell_height, bg=cell_bg_color, bd=1, relief='solid')
        time_and_date_label.grid(row=i + 2, column=j + 1)

root.mainloop()
