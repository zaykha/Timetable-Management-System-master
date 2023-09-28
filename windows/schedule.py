import sqlite3
import tkinter as tk
from tkinter import ttk
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import filedialog, messagebox
from tkinter import Entry, Label
from tkinter import filedialog
import pandas as pd
from tkinter import messagebox
import random
import os
import csv
from datetime import datetime
# from tkcalendar import DateEntry
# from tkcalendar import Calendar
# from tkcalendar import Calendar, DateEntry
from operator import itemgetter
from tkinter import font
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

'''
    LIST OF FUNCTIONS USED FOR VARIOUS FUNCTIONS THROUGH TKinter INTERFACE
        * create_treeview()
        * update_treeview()
        * parse_data()
        * update data()
        * remove_data()
        * show_passw()
'''



# Create a variable to keep track of the current sorting order (0 for ascending, 1 for descending)
current_sort_order = 0
# Define a global string variable
selected_description = ""
selected_duration = ""
selected_planned_size = ""
selected_allocate_staffname = ""
filtered_results1 = []
file_paths = {}

def run_tt_s(): os.system('py windows\\timetable_viewer.py "{data}"')

def clear_treeview():
    # Delete all items (rows) in the Treeview
    tree.delete(*tree.get_children())

def display_search_results(results):
    clear_treeview()
    # Sort the data by the Schedule date (assuming it's in the 4th column)
    results.sort(key=lambda row: datetime.strptime(row[3], "%d/%m/%Y"))

    for item in results:
        
     tree.insert("", "end", values=item) 


    
# create treeview (call this function once)
def create_treeview():
    
    tree['columns'] = list(map(lambda x: '#' + str(x), range(1, 11)))
    tree.column("#0", width=5, stretch=tk.NO)
    tree.column("#1", width=80, stretch=tk.NO)
    tree.column("#2", width=80, stretch=tk.NO)
    tree.column("#3", width=80, stretch=tk.NO)
    tree.column("#4", width=80, stretch=tk.NO)
    tree.column("#5", width=80, stretch=tk.NO)
    tree.column("#6", width=80, stretch=tk.NO)
    tree.column("#7", width=80, stretch=tk.NO)
    tree.column("#8", width=80, stretch=tk.NO)
    tree.column("#9", width=80, stretch=tk.NO)
    tree.column("#10", width=80, stretch=tk.NO)
    tree.heading('#0', text="No.",anchor='center')
    tree.heading('#1', text="Module",anchor='center')
    tree.heading('#2', text="Description",anchor='center')
    tree.heading('#3', text="Activity Dates (Individual)",anchor='center')
    tree.heading('#4', text="Scheduled Start Time",anchor='center')
    tree.heading('#5', text="Scheduled End Time",anchor='center')
    tree.heading('#6', text="Duration",anchor='center')
    tree.heading('#7', text="Allocated Location Name",anchor='center')
    tree.heading('#8', text="Planned Size",anchor='center')
    tree.heading('#9', text="Allocated Staff Name",anchor='center')
    tree.heading('#10', text="Lecturer",anchor='center')
    tree['height'] = 15
    tree.place(x=530, y=100)



def check_select_file():
    selected_item = file_list.curselection()
    if not selected_item:
        messagebox.showwarning("Select file", " Please select CSV file!")
    else:
         load_selected_schedule()

def load_selected_schedule():
    
    selected_indexes = file_list.curselection()
    if not selected_indexes:
        messagebox.showwarning("Select a File", "Please select a CSV file from the list.")
        
        return

    selected_index = selected_indexes[0] if selected_indexes else None

    if selected_index is not None and 0 <= selected_index < len(file_list.get(0, tk.END)):
        selected_file_name = file_list.get(selected_index)
        selected_file_path = file_paths.get(selected_file_name)

        if selected_file_path:
            clear_treeview()
            load_schedule(selected_file_path)
            
        else:
            
            messagebox.showerror("File Not Found", f"File path for '{selected_file_name}' not found.")
    else:
        
        messagebox.showerror("Invalid Selection", "Invalid or out-of-range selection in the listbox.")

# Modify the load_schedule function
def load_schedule(file_name):
    # Read and insert data from the CSV file
    create_treeview()
    file_path = file_name

    try:
        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  # Read the header row
            data = list(csv_reader)

            # Sort the data by the Schedule date (assuming it's in the 4th column)
            data.sort(key=lambda row: datetime.strptime(row[3], "%d/%m/%Y"))

            # Insert the sorted data into the Treeview
            for row in data:
                tree.insert('', 'end', values=row)

    except FileNotFoundError:
        print("File not found:", file_path)
    except Exception as e:
        print("An error occurred:", str(e))
        tree.place(x=530, y=100)

# ... (Rest of your code)



def search_and_display_schedule():
 row_count = len(tree.get_children())
 if row_count == 0:
    messagebox.showerror("Error","List of Schedule is empty")
 else:  
    filtered_results = []
    global selected_description
    global selected_duration
    global selected_planned_size
    global selected_allocate_staffname
    selected_module = module_var.get().strip().lower()
    selected_lecturer = lecturer_var.get().strip().lower()
    selected_location = location_var.get().strip().lower()
    start_date_str = start_date_var.get()
    end_date_str = end_date_var.get()
     # Parse user-entered date strings into datetime objects
    selected_start_date = datetime.strptime(start_date_str, "%d/%m/%Y") if start_date_str else None
    selected_end_date = datetime.strptime(end_date_str, "%d/%m/%Y") if end_date_str else None
    selected_start_time = start_time_var.get()
    selected_end_time = end_time_var.get()
    selected_day = day_var.get().strip().lower()
    selected_other = other_var.get()
    selected_others = other_vars.get().strip().lower()
    if(selected_other == "Description"):
      selected_description = selected_others
    if(selected_other == "Duration"):
        selected_duration = selected_others 
    if(selected_other == "Planned Size"):
        selected_planned_size = selected_others 
    if(selected_other == "Allocated Staff Name"):
        selected_allocate_staffname = selected_others   
    if (selected_start_date is not None and selected_end_date is not None):
         if selected_start_date > selected_end_date:
           messagebox.showerror("Error", "Start date cannot be greater than end date")
    if ((selected_start_date != "") and  (selected_end_date == "")):
        messagebox.showwarning("Infomation", "please select End Date.")
    if ((selected_start_date == "") and  (selected_end_date != "")):
        messagebox.showwarning("Infomation", "please select Start Date.")
    if ((selected_start_time != "") and  (selected_end_time == "")):
              messagebox.showwarning("Infomation", "please enter End time.")
    if ((selected_start_time == "") and  (selected_end_time != "")):
              messagebox.showwarning("Infomation", "please enter Start time.")    
    # Perform the search and display the results
    for entry in tree.get_children():
      item_data = tree.item(entry, 'values')
     #if item_data:
      no = item_data[0]
      module_name = item_data[1].lower()
      description = item_data[2].lower()
      schedule_date = item_data[3]
      scheduled_days = item_data[4].lower()
      scheduled_starttime = item_data[5]
      scheduled_end_time = item_data[6]
      duration = item_data[7].lower()
      location = item_data[8].lower()
      planned_size = item_data[9].lower()
      allocated_staff_name = item_data[10].lower()
      lecturer_name = item_data[11].lower() 
      item_date = datetime.strptime(schedule_date, "%d/%m/%Y") 
      
      date_condition = (not selected_start_date or not selected_end_date or (selected_start_date <= item_date <= selected_end_date))
      module_condition = (selected_module == "" or module_name == selected_module)
      lecturer_condition = (selected_lecturer == "" or lecturer_name == selected_lecturer)
      location_condition = (selected_location == "" or location == selected_location)
      duration_condition = (selected_duration == "" or duration == selected_duration)
      plan_size_condition = (selected_planned_size == "" or planned_size == selected_planned_size)
      staff_name_condition = (selected_allocate_staffname == "" or allocated_staff_name == selected_allocate_staffname)
      description_condition = (selected_description == "" or description == selected_description)
      day_condition = (selected_day == "" or selected_day == scheduled_days)
      time_condition = (
      (not selected_start_time or scheduled_starttime >= selected_start_time) and
      (not selected_end_time or scheduled_end_time <= selected_end_time)
      )
      if date_condition and module_condition and lecturer_condition and location_condition and duration_condition and plan_size_condition and staff_name_condition and description_condition and day_condition and time_condition :
        filtered_results.append(item_data)
        
    # Call another function to display the filtered results
    display_search_results(filtered_results)

# Create a function to be executed when the button is clicked
def browse_directory():
    directory_path = filedialog.askdirectory()
    if not directory_path:
        messagebox.showerror("File Not Found", f"File path for '{directory_path}' not found.")
    else:    
        
        # Check if there are any CSV files in the selected directory
        csv_files = [file for file in os.listdir(directory_path) if file.endswith(".csv")]

        if not csv_files:
           messagebox.showerror("File Not Found", f"File path for '{directory_path}' not found.") 
        else:
            
            for csv_file in csv_files:
                list_files(directory_path)
        

# Populate the Listbox with CSV file names in the directory
def list_files(directory_path):
    file_list.delete(0, tk.END)  # Clear the listbox
    try:
        files = os.listdir(directory_path)
        for file in files:
            if file.lower().endswith('.csv'):
                file_paths[file] = os.path.join(directory_path, file)  # Store the full path
                file_list.insert(tk.END, file)
    except Exception as e:
        file_list.insert(tk.END, f"Error: {str(e)}")
   
def show_selected_data():
    selected_items = tree.selection()
    selected_data = []
    
    for item in selected_items:
        values = tree.item(item, 'values')
        selected_data.append(values)

    if selected_data:
        run_tt_s(selected_data)

def show_selected_schedule_data():
   
    selected_items = tree.selection()
    selected_data = []

    for item in selected_items:
        try:
            values = tree.item(item, 'values')
            selected_data.append(values)
        except tk.TclError as e:
            print(f"Error: {e} - Item {item} not found")

    if selected_data:
        show_selected_data_window(selected_data)
        

def generate_pdf(selected_data, file_path):
    # Create a PDF file at the specified location
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    
    # Create a list to hold the data for the table
    data = []
    session_data = []
    # Data for the first table
    weeks = ["","Week1", "Week2", "Week3", "Week4", "Week5", "Week6", "Week7", "Week8", "Week9", "Week10"]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    # Add a header row to the data list
    header = ["Module", "Lecturer", "Module Schedule", "Remark"]
    data.append(header)

    # Iterate through the Treeview data and add it to the data list
    for i, data_row in enumerate(selected_data, start=1):
        # Append each row as a list to the data list
        
        name = data_row[1]
        description = data_row[2]
        # Perform string splitting and extraction
        module = name.split('_')
        # Remove "SET" from description
        module_desc = description.replace("SET", "").strip() 
        result_module = None  # Initialize result_module as None

        if len(module) == 5:
            result_module = module[3]
            module_schedule = module[4]
        final_module = result_module + " " +  module_desc 
        final_module_schedule = module_schedule
        # Create a new list containing the data to append
        row_to_append = [final_module, data_row[10], final_module_schedule,data_row[8]]
    
        # Append the new list to the data list
        data.append(row_to_append)

    # Create a table and specify its style
    table = Table(data, colWidths=152, rowHeights=30)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),  # Font size for the header row
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),  # Font size for data rows
    ]))

    for i, data in enumerate(selected_data, start=1):
        name = data[1]
        # Perform string splitting and extraction
        module = name.split('_')
        result_module = None  # Initialize result_module as None
        module_schedule = ""  # Initialize module_schedule as an empty string

        if len(module) == 5:
            result_module = module[3]
            module_schedule = module[4]

        module_code = result_module
        final_module_schedule = module_schedule
        start_time = data[5]
        end_time = data[6]
        format_start_time = start_time[:-3]  # Remove the last three characters
        format_end_time = end_time[:-3]
        final_session_time = str(format_start_time) + "-" + str(format_end_time)
        days = data[4]
        date = data[3]

         # Create a new list containing the data to append
        row_to_session_append = [final_session_time, module_code,days,date, final_module_schedule]
    
        # Append the new list to the data list
        session_data.append(row_to_session_append)
        
    # Data for the second table
    weeks = ["","Week1", "Week2", "Week3", "Week4", "Week5", "Week6", "Week7", "Week8", "Week9", "Week10"]
    days_name = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    table_data_session = [[week] + days_name for week in weeks]
    # Create a table for the second set of data
    table_session = Table(table_data_session, colWidths=110, rowHeights=40)
    
    # Define the style for the second table
    table_style_session = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),  # Font size for the header row
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 8),  # Font size for data rows
        ('ALIGN', (0, 1), (-1, -1), 'CENTER')  # Align data rows to center
])
    session_times = {}
    # Apply the style to the second table
    table_session.setStyle(table_style_session)
    # Add session_data to the table
    for row_index, row_data in enumerate(session_data):
        for col_index, cell_data in enumerate(row_data):
            # Update the cell in table_session with the corresponding data from session_data
            table_session._argW[col_index + 1] = 50  # Adjust the column width if necessary
            table_session.setStyle(TableStyle([('TEXTCOLOR', (col_index + 1, row_index + 1), (col_index + 1, row_index + 1), colors.black)]))
            session_time, module_code, days, date, session_name = row_data[0], row_data[1], row_data[2], row_data[3], row_data[4]
            key = f"{days}_{date}"  # Create a key by combining day and date
            if key not in session_times:
                session_times[key] = []  # Initialize an empty list for this day and date
                session_times[key].append(session_time)
            
   
    # Convert the session times to a delimited string
    for key, times in session_times.items():
        session_times[key] = '|'.join(times)
    for j in range(len(weeks)): 
     for row_index, row_data in enumerate(session_data):
        for col_index, cell_data in enumerate(row_data):
            session_time, module_code,days,date, session_name= row_data[0], row_data[1], row_data[2],row_data[3],row_data[4]
           
            key = f"{days}_{date}"
            day_date_session = session_times.get(key, "")  # Get the session times for this day and date
            
            if days == days_name[0] :
                    session_text = day_date_session if day_date_session and day_date_session.strip() != "" else "-"
                    module_text = module_code if module_code and module_code.strip() != "" else "-"
                    session_name_text = session_name if session_name and session_name.strip() != "" else "-"
                    cell_content = Paragraph(f"{session_text}\n{date}\n{module_text}\n{session_name_text}", getSampleStyleSheet()['Normal'])
                    # Set the cell content
                    table_session._argW[col_index + 1] = 100  # Adjust the column width if necessary
                    table_session.setStyle(TableStyle([('TEXTCOLOR', (col_index + 1, row_index + 1), (col_index + 1, row_index + 1), colors.black)]))
                    table_session._cellvalues[row_index + 1][1] = cell_content
            elif days == days_name[1]:
                    session_text = day_date_session if day_date_session and day_date_session.strip() != "" else "-"
                    module_text = module_code if module_code and module_code.strip() != "" else "-"
                    session_name_text = session_name if session_name and session_name.strip() != "" else "-"
                    cell_content = Paragraph(f"{session_text}\n{date}\n{module_text}\n{session_name_text}", getSampleStyleSheet()['Normal'])
                    # Set the cell content
                    table_session._argW[col_index + 1] = 100  # Adjust the column width if necessary
                    table_session.setStyle(TableStyle([('TEXTCOLOR', (col_index + 1, row_index + 1), (col_index + 1, row_index + 1), colors.black)]))
                    table_session._cellvalues[row_index + 1][2] = cell_content
            elif days == days_name[2]:
                    session_text = day_date_session if day_date_session and day_date_session.strip() != "" else "-"
                    module_text = module_code if module_code and module_code.strip() != "" else "-"
                    session_name_text = session_name if session_name and session_name.strip() != "" else "-"
                    cell_content = Paragraph(f"{session_text}\n{date}\n{module_text}\n{session_name_text}", getSampleStyleSheet()['Normal'])
                    # Set the cell content
                    table_session._argW[col_index + 1] = 100  # Adjust the column width if necessary
                    table_session.setStyle(TableStyle([('TEXTCOLOR', (col_index + 1, row_index + 1), (col_index + 1, row_index + 1), colors.black)]))
                    table_session._cellvalues[row_index + 1][3] = cell_content
            elif days == days_name[3]:
                    session_text = day_date_session if day_date_session and day_date_session.strip() != "" else "-"
                    module_text = module_code if module_code and module_code.strip() != "" else "-"
                    session_name_text = session_name if session_name and session_name.strip() != "" else "-"
                    cell_content = Paragraph(f"{session_text}\n{date}\n{module_text}\n{session_name_text}", getSampleStyleSheet()['Normal'])
                    # Set the cell content
                    table_session._argW[col_index + 1] = 100  # Adjust the column width if necessary
                    table_session.setStyle(TableStyle([('TEXTCOLOR', (col_index + 1, row_index + 1), (col_index + 1, row_index + 1), colors.black)]))
                    table_session._cellvalues[row_index + 1][4] = cell_content
            else:
                    session_text = day_date_session if day_date_session and day_date_session.strip() != "" else "-"
                    module_text = module_code if module_code and module_code.strip() != "" else "-"
                    session_name_text = session_name if session_name and session_name.strip() != "" else "-"
                    cell_content = Paragraph(f"{session_text}\n{date}\n{module_text}\n{session_name_text}", getSampleStyleSheet()['Normal'])
                    # Set the cell content
                    table_session._argW[col_index + 1] = 100  # Adjust the column width if necessary
                    table_session.setStyle(TableStyle([('TEXTCOLOR', (col_index + 1, row_index + 1), (col_index + 1, row_index + 1), colors.black)]))
                    table_session._cellvalues[row_index + 1][5] = cell_content
                
            if days != days_name[0] or days != days_name[1] or days != days_name[2] or days != days_name[3] or days != days_name[4] :
                
                    cell_content = Paragraph("", getSampleStyleSheet()['Normal'])
                    # Set the cell content
                    table_session._argW[col_index + 1] = 100  # Adjust the column width if necessary
                    table_session.setStyle(TableStyle([('TEXTCOLOR', (col_index + 1, row_index + 1), (col_index + 1, row_index + 1), colors.black)]))
                    table_session._cellvalues[j][col_index+1] = cell_content
                        
                               
                        
                        
    # Create a list to hold both tables
    combined_tables = [table, table_session]
    # Build the PDF document with both tables
    doc.build(combined_tables)
   
def validate_date_input(input_text):
    # This function is used to validate date input format (dd/mm/yyyy).
    parts = input_text.split("/")
    if len(parts) != 3:
        return False
    day, month, year = parts
    if not (day.isdigit() and month.isdigit() and year.isdigit()):
        return False
    day, month, year = int(day), int(month), int(year)
    if month < 1 or month > 12 or day < 1 or day > 31 or year < 1900:
        return False
    return True

def on_date_entry_change(event, var, error_label):
    # This function is called whenever a key is pressed in the Entry widget.
    # It validates the input and displays an error message if it's invalid.
    date_text = var.get()
    error_label.config(text="")
    
    if date_text.count("/") == 2:
        # Check if all segments are digits before validating the date format
        parts = date_text.split("/")
        if not all(part.isdigit() for part in parts):
            error_label.config(text="Invalid Date Format (dd/mm/yyyy)", fg="red")
            return
    
    if not validate_date_input(date_text):
        error_label.config(text="Invalid Date Format", fg="red")


def show_selected_data_window(selected_data):
    global filtered_results1
    selected_data_window = tk.Toplevel(subtk)
    selected_data_window.title("Timetable Viewer and Generator")
    
    # Create a Canvas widget to hold the content
    canvas = tk.Canvas(selected_data_window)
    canvas.grid(row=0, column=0, sticky="nsew")

    # Create a vertical scrollbar
    scrollbar = tk.Scrollbar(selected_data_window,orient="vertical", command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")

    # Configure the canvas to work with the scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas to hold your content
    content_frame = tk.Frame(canvas)
    scrollbar.grid(row=0, column=1, sticky="ns")
    
    # Create buttons for PDF and Excel generation
    pdf_button = tk.Button(selected_data_window, text="Generate PDF", font=('Consolas', 12),
                           command=lambda: generate_pdf(selected_data, filedialog.asksaveasfilename(
                               defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")]))
                           )
    pdf_button.grid(row=1, column=0)
    excel_button = tk.Button(selected_data_window, text="Generate Excel", font=('Consolas', 12), command="")

    # Place the buttons using the grid() method
    
    excel_button.grid(row=1, column=1)

    # Create a single frame to hold both the schedule grid and module information
    frame = tk.Frame(selected_data_window)
    frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
    # Define the number of days and periods
    days = 5
    week = 12

    # Create labels for day names and period names
    day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    period_names = list(map(lambda x: 'Week ' + str(x), range(1, week + 1)))
   
    
    # Create a Treeview widget for module information
    module_treeview = ttk.Treeview(frame, columns=(1, 2, 3, 4), show="headings", displaycolumns=(1, 2, 3, 4))
    module_treeview.heading(1, text="Module")  # Set the column name
    module_treeview.heading(2, text="Lecturer")
    module_treeview.heading(3, text="Module Schedule")
    module_treeview.heading(4, text="Remarks")
    module_treeview.column(1, minwidth=100, width=290,anchor='center')  # Set a non-zero minwidth
    module_treeview.column(2, minwidth=100, width=290,anchor='center')
    module_treeview.column(3, minwidth=200, width=290,anchor='center')
    module_treeview.column(4, minwidth=100, width=290,anchor='center')
    for i, data in enumerate(selected_data, start=1):
        name = data[1]
        description = data[2]
        # Perform string splitting and extraction
        module = name.split('_')
        # Remove "SET" from description
        module_desc = description.replace("SET", "").strip() 
        result_module = None  # Initialize result_module as None

        if len(module) == 5:
            result_module = module[3]
            module_schedule = module[4]
        final_module = result_module + " " +  module_desc 
        final_module_schedule = module_schedule
        module_treeview.insert("", "end", values=(final_module, data[10], final_module_schedule,data[8]))
 
      #module_treeview.insert("", "end", values=items[1:])
    # Place the Treeview widget using the grid() method
    module_treeview.grid(row=0, column=0, columnspan=len(day_names) + 1)
    
    # Create a Treeview widget with sample data (you can replace this with your actual data)
    schedule_treeview = ttk.Treeview(frame, columns=["Session Time", "Module Code","Days","Date", *day_names])
    
    for i, data in enumerate(selected_data, start=1):
        name = data[1]
        # Perform string splitting and extraction
        module = name.split('_')
        result_module = None  # Initialize result_module as None
        module_schedule = ""  # Initialize module_schedule as an empty string

        if len(module) == 5:
            result_module = module[3]
            module_schedule = module[4]

        module_code = result_module
        final_module_schedule = module_schedule
        start_time = data[5]
        end_time = data[6]
        format_start_time = start_time[:-3]  # Remove the last three characters
        format_end_time = end_time[:-3]
        final_session_time = str(format_start_time) + "-" + str(format_end_time)
        days = data[4]
        date = data[3]

        # Update the last final_module_schedule for each iteration
    
        schedule_treeview.insert("", "end", values=[final_session_time, module_code,days,date] + [final_module_schedule] * len(day_names))
    # Calculate the width for the columns
    column_width = 30  # Adjust this width as needed

    # Create labels for day names (top row)
    for i, day in enumerate(day_names):
        label = tk.Label(frame, text=day, width=column_width, height=2, bg='yellow', bd=1, relief='solid')
        label.grid(row=1, column=i + 1)

    # Create labels for period names (left column)
    for i, period in enumerate(period_names):
        label = tk.Label(frame, text=period, width=10, height=5, bg='yellow', bd=1, relief='solid')
        label.grid(row=i + 2, column=0)  # First column
    session_times = {}
    
    for i, item in enumerate(schedule_treeview.get_children()):
        values = schedule_treeview.item(item, "values")
        session_time, module_code, days, date, session_name = values[0], values[1], values[2], values[3], values[4]
        key = f"{days}_{date}"  # Create a key by combining day and date
        if key not in session_times:
            session_times[key] = []  # Initialize an empty list for this day and date
        session_times[key].append(session_time)
    
    # Convert the session times to a delimited string
    for key, times in session_times.items():
        session_times[key] = '|'.join(times)
        
    # Create labels for module name, time slots, and schedule date from the Treeview data
    for i, item in enumerate(schedule_treeview.get_children()):
        values = schedule_treeview.item(item, "values")
        
        session_time, module_code,days,date, session_name= values[0], values[1], values[2],values[3],values[4]
        key = f"{days}_{date}"
        day_date_session = session_times.get(key, "")  # Get the session times for this day and date
        for j in range(len(day_names)):
            
            if days == day_names[0] :
                module_text = module_code if module_code and module_code.strip() != "" else "-"
                
                # Set the same row height for all rows
                cell_height = 5
                time_and_date_label = tk.Label(frame, text=f"{day_date_session}\n{date}\n{module_text}\n{session_name}", width=column_width, height=cell_height, bd=1, relief='solid')
                time_and_date_label.grid(row=i + 2, column=1)   
               
            elif days == day_names[1]:
                
                module_text = module_code if module_code and module_code.strip() != "" else "-"
                
                # Set the same row height for all rows
                cell_height = 5
                time_and_date_label = tk.Label(frame, text=f"{day_date_session}\n{date}\n{module_text}\n{session_name}", width=column_width, height=cell_height, bd=1, relief='solid')
                time_and_date_label.grid(row=i + 2, column=2)   
                
            elif days == day_names[2]:
                
                module_text = module_code if module_code and module_code.strip() != "" else "-"
                
                # Set the same row height for all rows
                cell_height = 5
                time_and_date_label = tk.Label(frame, text=f"{day_date_session}\n{date}\n{module_text}\n{session_name}", width=column_width, height=cell_height, bd=1, relief='solid')
                time_and_date_label.grid(row=i + 2, column=3) 
                  
            elif days == day_names[3]:
                
                module_text = module_code if module_code and module_code.strip() != "" else "-"
                
                # Set the same row height for all rows
                cell_height = 5
                time_and_date_label = tk.Label(frame, text=f"{day_date_session}\n{date}\n{module_text}\n{session_name}", width=column_width, height=cell_height, bd=1, relief='solid')
                time_and_date_label.grid(row=i + 2, column=4)
            
            else:       
                
                module_text = module_code if module_code and module_code.strip() != "" else "-"
                
                # Set the same row height for all rows
                cell_height = 5
                time_and_date_label = tk.Label(frame, text=f"{day_date_session}\n{date}\n{module_text}\n{session_name}", width=column_width, height=cell_height, bd=1, relief='solid')
                time_and_date_label.grid(row=i + 2, column=5)   
    # Update the canvas scrolling region when the content changes
    content_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))
    selected_data_window.grid_rowconfigure(0, weight=1)
    selected_data_window.grid_columnconfigure(0, weight=1)        

# main
if __name__ == "__main__":  

    '''
        DATABASE CONNECTIONS AND SETUP
    '''

    # connecting database
    conn = sqlite3.connect(r'files/timetable.db')

    # creating Tabe in the database
    conn.execute('CREATE TABLE IF NOT EXISTS STUDENT\
    (SID CHAR(10) NOT NULL PRIMARY KEY,\
    PASSW CHAR(50) NOT NULL,\
    NAME CHAR(50) NOT NULL,\
    ROLL INTEGER NOT NULL,\
    SECTION CHAR(5) NOT NULL)')


    '''
        TKinter WINDOW SETUP WITH WIDGETS
            * Label(1-11)
            * Entry(6)
            * ComboBox(1-2)
            * Treeview(1)
            * Button(1-3)
    '''

    # TKinter Window
    subtk = tk.Tk()
    subtk.geometry('1300x600')
    subtk.title('Schedule Listing')
    # Maximize the window
    subtk.state('zoomed')
    # Set directory_path to the current working directory
    directory_path = os.getcwd()
    # Label1
    tk.Label(
        subtk,
        text='List of Schedule',
        font=('Consolas', 20, 'bold')
    ).place(x=620, y=50)

    # Label2
    tk.Label(
        subtk,
        text='Search Criteria',
        font=('Consolas', 20, 'bold')
    ).place(x=110, y=50)

    # Label3
    tk.Label(
        subtk,
        text='Search information in the following prompt!',
        font=('Consolas', 10, 'italic')
    ).place(x=110, y=85)
    
    # Create a button to browse for a directory
    browse_button = tk.Button(subtk, text="Browse Directory",font=('Consolas', 12) ,command=browse_directory)
    browse_button.place(x=525,y=430)

    # Create a listbox to display files in the selected directory
    file_list = tk.Listbox(subtk,width=30,height=10)
    file_list.place(x=685,y= 430)
    
    # Add a button to load the selected schedule
    load_button = tk.Button(subtk, text="Load Selected Schedule",font=('Consolas', 12), command=check_select_file)
    load_button.place(x=870,y=430)

    # Add a button to load Timetable depend on the selected schedule
    timetable_button = tk.Button(subtk, text="Timetable Viewer",font=('Consolas', 12), command=show_selected_schedule_data)
    timetable_button.place(x=1100,y=430)

    # Label4
    tk.Label(
        subtk,
        text='Module:',
        font=('Consolas', 12)
    ).place(x=100, y=130)

    # Entry1
    module_var = tk.StringVar()
    module_entry = tk.Entry(
        subtk,
        font=('Consolas', 12),textvariable=module_var,
        width=15
    )
    module_entry.place(x=285, y=130)

    # Label5
    tk.Label(
        subtk,
        text='Lecturer:',
        font=('Consolas', 12)
    ).place(x=100, y=170)

    # Entry2
    lecturer_var = tk.StringVar()
    lecturer_entry = tk.Entry(
        subtk,
        font=('Consolas', 12),textvariable=lecturer_var,
        width=15,
        
    )
    lecturer_entry.place(x=285, y=170)

   

    # Label6
    tk.Label(
        subtk,
        text='Location:',
        font=('Consolas', 12)
    ).place(x=100, y=210)

    # Entry3
    location_var = tk.StringVar()
    location_entry = tk.Entry(
        subtk,
        font=('Consolas', 12),textvariable=location_var,
        width=15,
        
    )
    location_entry.place(x=285, y=210)



    # Label8
    tk.Label(
        subtk,
        text='Start Date:',
        font=('Consolas', 12)
    ).place(x=100, y=250)

    # Entry5
    start_date_var = tk.StringVar()
    # start_date_entry = DateEntry(subtk,textvariable=start_date_var, date_pattern="dd/mm/yyyy")
    start_date_entry = Entry(
        subtk,
        textvariable=start_date_var,
    )
    start_date_entry.delete(0, "end")
    start_date_entry.place(x=285, y=250)
    # start_date_var.trace("w", on_date_entry_change)
    # Bind validation function to the Entry widgets for Start Date

  # Error message label for Start Date
    error_message_start = Label(
        subtk,
        text="",
        fg="red"
    )
    error_message_start.pack()

    # Label9
    tk.Label(
        subtk,
        text='End Date:',
        font=('Consolas', 12)
    ).place(x=100, y=290)

    # Entry6
    end_date_var = tk.StringVar()
    # end_date_entry = DateEntry(subtk,textvariable=end_date_var, date_pattern="dd/mm/yyyy")
    end_date_entry = Entry(
        subtk,
        textvariable=end_date_var,
    )
    end_date_entry.delete(0, "end")
    end_date_entry.place(x=285, y=290)
    # end_date_var.trace("w", on_date_entry_change)
    end_date_entry.bind("<KeyRelease>", on_date_entry_change)

    # Error message label for End Date
    error_message_end = Label(
        subtk,
        text="",
        fg="red"
    )
    error_message_end.pack()

    # Bind validation function to the Entry widgets for Start Date
    start_date_entry.bind("<KeyRelease>", lambda event, var=start_date_var, error_label=error_message_start: on_date_entry_change(event, var, error_label))

    # Bind validation function to the Entry widgets for End Date
    end_date_entry.bind("<KeyRelease>", lambda event, var=end_date_var, error_label=error_message_end: on_date_entry_change(event, var, error_label))

    # Label10
    tk.Label(
        subtk,
        text='Start Time (HH:MM:SS)',
        font=('Consolas', 12)
    ).place(x=100, y=330)

    # Entry7
    start_time_var = tk.StringVar()
    start_time_entry = tk.Entry(
        subtk,
        font=('Consolas', 12),textvariable=start_time_var,
        width=10,
    )
    start_time_entry.place(x=285, y=330)
    
    # Label11
    tk.Label(
        subtk,
        text='End Time (HH:MM:SS)',
        font=('Consolas', 12)
    ).place(x=100, y=370)

    # Entry8
    end_time_var = tk.StringVar()
    end_time_entry = tk.Entry(
        subtk,
        font=('Consolas', 12),textvariable=end_time_var,
        width=10,
    )
    end_time_entry.place(x=285, y=370)
    
      # Label12
    tk.Label(
        subtk,
        text='Day',
        font=('Consolas', 12)
    ).place(x=100, y=410)

    # Entry9
    day_var = tk.StringVar()
    day_dropdown = ttk.Combobox(
    subtk,textvariable=day_var,
    values=["","Monday","Tuesday","Wednesday","Thursday","Friday"]
    )
    day_dropdown.pack(pady=15)
    day_dropdown.current(0)
    day_dropdown.place(x=285, y=410)
    
    
      # Label13
    tk.Label(
        subtk,
        text='Other',
        font=('Consolas', 12)
    ).place(x=100, y=450)

    # Entry10
    other_var = tk.StringVar()
    combo_other = ttk.Combobox(
    subtk,textvariable=other_var,
    values=["","Description","Duration","Planned Size","Allocated Staff Name"]
    )
    combo_other.pack(pady=15)
    combo_other.current(0)
    combo_other.place(x=285, y=450)

    other_vars = tk.StringVar()
    other_entry = tk.Entry(
        subtk,
        font=('Consolas', 12),textvariable=other_vars,
        width=10,
    )
    other_entry.place(x=428, y=450)
    
    # Button1
    B1 = tk.Button(
        subtk,
        text='Search',
        font=('Consolas', 12),
        command=search_and_display_schedule
    )
    B1.place(x=190,y=540)

    
    
    
    # Treeview1
    tree = ttk.Treeview(subtk)
    create_treeview()
    
     # Add vertical scrollbar
    vscroll = ttk.Scrollbar(subtk, orient="vertical", command=tree.yview)
    vscroll.pack(side="right", fill="y")
    tree.configure(yscrollcommand=vscroll.set)

    # Add horizontal scrollbar
    hscroll = ttk.Scrollbar(subtk, orient="horizontal", command=tree.xview)
    hscroll.pack(side="bottom", fill="x")
    tree.configure(xscrollcommand=hscroll.set)
     
    # looping Tkiniter window
    subtk.mainloop()
    conn.close() # close database after all operations
