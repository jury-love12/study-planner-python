import webbrowser
import tkinter as tk
import mysql.connector
from tkinter import ttk, messagebox

# MySQL connection configuration
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''
MYSQL_DATABASE = 'group1'

# Open Google Calendar in the default web browser
def open_calendar():
    webbrowser.open('https://calendar.google.com/calendar/r')

def open_tasks():
    try:
        # Establish MySQL connection
        connection = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )

        # Create a cursor to execute MySQL queries
        cursor = connection.cursor()

        # Execute your tasks query
        cursor.execute('SELECT * FROM tasks')

        # Fetch all tasks from the result set
        tasks = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        # Display tasks in a treeview
        display_tasks(tasks)

    except mysql.connector.Error as error:
        print('An error occurred: %s' % error)

    # Display tasks in a treeview


def display_tasks(tasks):
    def add_task():
        # Get values from entry widgets
        task_name = task_name_entry.get()
        subject = subject_entry.get()
        due_date = due_date_entry.get()
        priority = priority_entry.get()
        status = status_entry.get()
        notes = notes_entry.get()

        try:
            # Establish MySQL connection
            connection = mysql.connector.connect(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD,
                database=MYSQL_DATABASE
            )

            # Create a cursor to execute MySQL queries
            cursor = connection.cursor()

            # Prepare the INSERT query
            query = "INSERT INTO tasks (task_name, subject, due_date, priority, status, notes) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (task_name, subject, due_date, priority, status, notes)

            # Execute the INSERT query
            cursor.execute(query, values)

            # Commit the changes to the database
            connection.commit()

            # Close the cursor and connection
            cursor.close()
            connection.close()

            # Update treeview with the newly added task
            tree.insert("", tk.END, text="New Task", values=(task_name, subject, due_date, priority, status, notes))

            # Display a success message
            print("Task added successfully!")

        except mysql.connector.Error as error:
            # Display an error message
            print('An error occurred: %s' % error)

        # Clear entry widgets
        task_name_entry.delete(0, tk.END)
        subject_entry.delete(0, tk.END)
        due_date_entry.delete(0, tk.END)
        priority_entry.delete(0, tk.END)
        status_entry.delete(0, tk.END)
        notes_entry.delete(0, tk.END)

    def delete_task():
        selected_item = tree.selection()
        if selected_item:
            task_id = tree.item(selected_item)['text']
            try:
                # Establish MySQL connection
                connection = mysql.connector.connect(
                    host=MYSQL_HOST,
                    user=MYSQL_USER,
                    password=MYSQL_PASSWORD,
                    database=MYSQL_DATABASE
                )

                # Create a cursor to execute MySQL queries
                cursor = connection.cursor()

                # Prepare the DELETE query
                query = "DELETE FROM tasks WHERE task_id = %s"
                values = (task_id,)

                # Execute the DELETE query
                cursor.execute(query, values)

                # Commit the changes to the database
                connection.commit()

                # Close the cursor and connection
                cursor.close()
                connection.close()

                # Remove the selected task from the treeview
                tree.delete(selected_item)

                # Display a success message
                print("Task deleted successfully!")

            except mysql.connector.Error as error:
                # Display an error message
                print('An error occurred: %s' % error)

    def update_task():
        selected_item = tree.selection()
        if selected_item:
            task_id = tree.item(selected_item)['text']
            # Get values from entry widgets
            task_name = task_name_entry.get()
            subject = subject_entry.get()
            due_date = due_date_entry.get()
            priority = priority_entry.get()
            status = status_entry.get()
            notes = notes_entry.get()

            try:
                # Establish MySQL connection
                connection = mysql.connector.connect(
                    host=MYSQL_HOST,
                    user=MYSQL_USER,
                    password=MYSQL_PASSWORD,
                    database=MYSQL_DATABASE
                )

                # Create a cursor to execute MySQL queries
                cursor = connection.cursor()

                # Prepare the UPDATE query
                query = "UPDATE tasks SET task_name = %s, subject = %s, due_date = %s, priority = %s, status = %s, notes = %s WHERE task_id = %s"
                values = (task_name, subject, due_date, priority, status, notes, task_id)

                # Execute the UPDATE query
                cursor.execute(query, values)

                # Commit the changes to the database
                connection.commit()

                # Close the cursor and connection
                cursor.close()
                connection.close()

                # Update the task in the treeview
                tree.item(selected_item, text=task_id, values=(task_name, subject, due_date, priority, status, notes))

                # Display a success message
                print("Task updated successfully!")

            except mysql.connector.Error as error:
                # Display an error message
                print('An error occurred: %s' % error)

    def on_task_select(event=None):
        selected_item = tree.selection()
        if selected_item:
            task_id = tree.item(selected_item)['text']
            task_info = tree.item(selected_item)['values']
            # Set the values in the entry widgets
            task_name_entry.delete(0, tk.END)
            task_name_entry.insert(0, task_info[0])

            subject_entry.delete(0, tk.END)
            subject_entry.insert(0, task_info[1])

            due_date_entry.delete(0, tk.END)
            due_date_entry.insert(0, task_info[2])

            priority_entry.delete(0, tk.END)
            priority_entry.insert(0, task_info[3])

            status_entry.delete(0, tk.END)
            status_entry.insert(0, task_info[4])

            notes_entry.delete(0, tk.END)
            notes_entry.insert(0, task_info[5])
        else:
            # Clear the entry widgets when no item is selected
            if root.focus_get() != tree:
                task_name_entry.delete(0, tk.END)
                subject_entry.delete(0, tk.END)
                due_date_entry.delete(0, tk.END)
                priority_entry.delete(0, tk.END)
                status_entry.delete(0, tk.END)
                notes_entry.delete(0, tk.END)

    root = tk.Tk()
    root.state('zoomed')  # Maximize the window
    root.resizable(False, False)

    tree = ttk.Treeview(root, columns=("task_name", "subject", "due_date", "priority", "status", "notes"))
    tree.heading("#0", text="Task ID")
    tree.heading("task_name", text="Task Name")
    tree.heading("subject", text="Subject")
    tree.heading("due_date", text="Due Date")
    tree.heading("priority", text="Priority")
    tree.heading("status", text="Status")
    tree.heading("notes", text="Notes")

    tree.column("#0", width=100)
    tree.column("task_name", width=150)
    tree.column("subject", width=100)
    tree.column("due_date", width=100)
    tree.column("priority", width=100)
    tree.column("status", width=100)
    tree.column("notes", width=200)

    for task in tasks:
        tree.insert("", tk.END, text=task[0], values=(task[1], task[2], task[3], task[4], task[5], task[6]))

    tree.pack(fill=tk.BOTH, expand=True)

    # Add entry widgets for task input
    input_frame = tk.Frame(root)
    input_frame.pack(pady=10)

    task_name_label = tk.Label(input_frame, text="Task Name:")
    task_name_label.grid(row=0, column=0, padx=5, pady=5)
    task_name_entry = tk.Entry(input_frame, width=50)
    task_name_entry.grid(row=0, column=1, padx=5, pady=5)

    subject_label = tk.Label(input_frame, text="Subject:")
    subject_label.grid(row=1, column=0, padx=5, pady=5)
    subject_entry = tk.Entry(input_frame, width=50)
    subject_entry.grid(row=1, column=1, padx=5, pady=5)

    due_date_label = tk.Label(input_frame, text="Due Date:")
    due_date_label.grid(row=2, column=0, padx=5, pady=5)
    due_date_entry = tk.Entry(input_frame, width=50)
    due_date_entry.grid(row=2, column=1, padx=5, pady=5)

    priority_label = tk.Label(input_frame, text="Priority:")
    priority_label.grid(row=3, column=0, padx=5, pady=5)
    priority_entry = tk.Entry(input_frame, width=50)
    priority_entry.grid(row=3, column=1, padx=5, pady=5)

    status_label = tk.Label(input_frame, text="Status:")
    status_label.grid(row=4, column=0, padx=5, pady=5)
    status_entry = tk.Entry(input_frame, width=50)
    status_entry.grid(row=4, column=1, padx=5, pady=5)

    notes_label = tk.Label(input_frame, text="Notes:")
    notes_label.grid(row=5, column=0, padx=5, pady=5)
    notes_entry = tk.Entry(input_frame, width=50)
    notes_entry.grid(row=5, column=1, padx=5, pady=5)

    # Add add button
    add_button = tk.Button(input_frame, text="Add Task", command=add_task)
    add_button.grid(row=6, column=0, padx=5, pady=5)

    # Add delete button
    delete_button = tk.Button(input_frame, text="Delete Task", command=delete_task)
    delete_button.grid(row=6, column=1, padx=5, pady=5)

    # Add update button
    update_button = tk.Button(input_frame, text="Update Task", command=update_task)
    update_button.grid(row=6, column=2, padx=5, pady=5)

    # Bind the on_task_select function to the treeview selection event
    tree.bind("<<TreeviewSelect>>", on_task_select)

    root.mainloop()

def create_button(parent, text, command):
    button = tk.Button(parent, text=text, command=command)
    button.pack(side=tk.LEFT, padx=10)  # Position the button with some padding on the left
    return button

def logout():
    # Functionality for logging out
    root.destroy()

def main():
    global root
    root = tk.Tk()
    root.geometry("500x400")
    root.resizable(False, False)

    # Create a label for "Student Homepage"
    label = tk.Label(root, text="Student Homepage", font=("Helvetica", 32))
    label.pack(pady=20)  # Position the label at the top with some padding

    # Create a frame to hold the buttons
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.BOTTOM, pady=20)  # Position the frame at the bottom with some padding

    # Create the "Open Calendar" button
    open_calendar_button = create_button(button_frame, "Open Calendar", open_calendar)
    open_calendar_button.config(height=2, width=20)  # Enlarge the button

    # Create the "Open Tasks" button
    open_tasks_button = create_button(button_frame, "Open Tasks", open_tasks)
    open_tasks_button.config(height=2, width=20)  # Enlarge the button

    # Create the "Logout" button
    logout_button = create_button(button_frame, "Logout", logout)
    logout_button.config(height=2, width=20)  # Enlarge the button

    root.mainloop()
if __name__ == '__main__':
    main()