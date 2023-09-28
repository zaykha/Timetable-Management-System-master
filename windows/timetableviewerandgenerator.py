import tkinter as tk
from tkinter import ttk
import pandas as pd
import sys
import json 


days = 5
periods = 6
period_names = list(map(lambda x: 'Period ' + str(x), range(1, 6+1)))
day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thrusday', 'Friday']

# Sample data for demonstration
data = {
    "Week": ["1", "2", "3", "4", "5", "6"],
    "Monday": ["9:00 AM - 10:00 AM", "10:15 AM - 11:15 AM", "Module A", "9:00 AM - 10:00 AM", "Module B", "Module C"],
    "Tuesday": ["Module D", "Module E", "Module F", "9:00 AM - 10:00 AM", "10:15 AM - 11:15 AM", "Module G"],
    "Wednesday": ["Module H", "9:00 AM - 10:00 AM", "Module I", "Module J", "Module K", "9:00 AM - 10:00 AM"],
    "Thursday": ["9:00 AM - 10:00 AM", "Module L", "Module M", "Module N", "Module O", "Module P"],
    "Friday": ["Module Q", "Module R", "10:15 AM - 11:15 AM", "Module S", "Module T", "Module U"],
}

# Extract column names
columns = list(data.keys())

def load_timetable(data):
    # Clear any existing data in the treeview
    for item in tree.get_children():
        tree.delete(item)

    # Insert data into the TreeView
    for name, time in data.items():
        tree.insert("", "end", values=(name, time))

# Initialize the main application window
root = tk.Tk()
root.title("Timetable Viewer")
# Maximize the window
root.state('zoomed')
style = ttk.Style()
style.configure("Custom.Treeview", rowheight=80)  # Adjust the row height (30 is an example)


# Create a pandas DataFrame from the sample data
df = pd.DataFrame(data)

# Create a Treeview widget to display the timetable
tree = ttk.Treeview(root, columns=columns, show="headings", style="Custom.Treeview")

# Configure column headings with colors
for i, col in enumerate(columns):
    col_tag = col.replace(" ", "")
    tree.heading(col, text=col, anchor='center')
    tree.column(col, width=200)
    tree.tag_configure(col_tag, anchor='center', background='lightblue', foreground='black')

# Apply background and foreground colors for specific rows (Week, Monday, Tuesday, Wednesday, Thursday, Friday)
for row in ["Week", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
    tree.tag_configure(row, background='blue', foreground='white')



# Create labels for additional information in a left-to-right tabular format
additional_info = {
    "Programming Title": "Introduction to Python",
    "Cohort": "Fall 2023",
    "Exam Venue": "Room 101",
}

row_index = 0
for key, value in additional_info.items():
    label_key = ttk.Label(root, text=key, font=("Arial", 10, "bold"))
    label_value = ttk.Label(root, text=value, font=("Arial", 10))
    
    label_key.grid(row=row_index, column=0, padx=10, pady=5, sticky="w")
    label_value.grid(row=row_index, column=1, padx=10, pady=5, sticky="w")
    
    row_index += 1

# Add labels for Module, Lecturer, Module Schedule and Remark
module_label = ttk.Label(root, text="Module", font=("Arial", 8, "bold"))
lecturer_label = ttk.Label(root, text="Lecturer", font=("Arial", 8, "bold"))
schedule_label = ttk.Label(root, text="Module Schedule", font=("Arial", 8, "bold"))
remark_label = ttk.Label(root, text="Remarks", font=("Arial", 8, "bold"))

# Add values for Module, Lecturer, and Module Schedule
module_value = ttk.Label(root, text="Python Programming Basics", font=("Arial", 8))
lecturer_value = ttk.Label(root, text="Dr. Smith", font=("Arial", 8))
schedule_value = ttk.Label(root, text="Monday to Friday, 9:00 AM - 12:00 PM", font=("Arial", 8))
remark_value = ttk.Label(root, text="Monday to Friday, 9:00 AM - 12:00 PM", font=("Arial", 8))

# Grid placement for Module, Lecturer, and Module Schedule labels and values
module_label.grid(row=row_index, column=0, padx=5, pady=5, sticky="w")
lecturer_label.grid(row=row_index, column=1, padx=5, pady=5, sticky="w")
schedule_label.grid(row=row_index, column=2, padx=5, pady=5, sticky="w")
remark_label.grid(row=row_index, column=3, padx=5, pady=5, sticky="w")

row_index += 1  # Move to the next row
module_value.grid(row=row_index, column=0, padx=5, pady=5, sticky="w")
lecturer_value.grid(row=row_index, column=1, padx=5, pady=5, sticky="w")
schedule_value.grid(row=row_index, column=2, padx=5, pady=5, sticky="w")
remark_value.grid(row=row_index, column=3, padx=5, pady=5, sticky="w")

# Grid placement for Treeview
tree.grid(row=row_index + 1, column=0, columnspan=3, padx=10, pady=10)

# Configure grid weights to make Treeview and labels expand with the window
root.grid_rowconfigure(row_index + 1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

# Start the Tkinter main loop
root.mainloop()

if __name__ == "__main__":
    # Parse the data passed as a command-line argument
    if len(sys.argv) > 1:
        data_string = sys.argv[1]
        data = json.loads(data_string)  # If you're passing data as JSON
    else:
        data = {}  # Default data when no argument is provided

    load_timetable(data)
